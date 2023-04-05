import os
import logging
from datetime import datetime

from apibara.indexer import IndexerRunner, IndexerRunnerConfiguration, Info
from apibara.indexer.indexer import IndexerConfiguration
from apibara.protocol.proto.stream_pb2 import Cursor, DataFinality
from apibara.starknet import EventFilter, Filter, StarkNetIndexer, felt
from apibara.starknet.cursor import starknet_cursor
from apibara.starknet.proto.starknet_pb2 import Block
from starknet_py.contract import ContractFunction
from apibara.starknet.proto.types_pb2 import FieldElement

from typing import List

from indexer.config import Config
from indexer.decoder import (
    decode_mint_adventurer_event,
    decode_update_adventurer_state_event,
    decode_adventurer_level_up_event,
    decode_discovery_event,
    decode_create_beast_event,
    decode_beast_state_event,
    decode_beast_level_up_event,
    decode_beast_attacked_event,
    decode_adventurer_attacked_event,
    decode_fled_beast_event,
    decode_adventurer_ambushed_event,
    decode_item_state_event,
    decode_item_xp_increase_event,
    decode_item_greatness_increase_event,
    decode_item_prefixes_assigned_event,
    decode_item_suffix_assigned_event,
    decode_claim_item_event,
    decode_item_merchant_update_event,
)
from indexer.utils import (
    felt_to_str,
    str_to_felt,
    check_exists_int,
    check_exists_timestamp,
    encode_int_as_bytes,
)

# Print apibara logs
root_logger = logging.getLogger("apibara")
# change to `logging.DEBUG` to print more information
root_logger.setLevel(logging.INFO)
root_logger.addHandler(logging.StreamHandler())


def encode_str_as_bytes(value):
    felt = str_to_felt(value)
    return felt.to_bytes(32, "big")


config = Config()


class LootSurvivorIndexer(StarkNetIndexer):
    def indexer_id(self) -> str:
        return "starknet-example"

    def initial_configuration(self) -> Filter:
        # Return initial configuration of the indexer.
        filter = Filter().with_header(weak=True)
        self.event_map = dict()

        def add_filter(contract, event):
            selector = ContractFunction.get_selector(event)
            self.event_map[selector] = event
            filter.add_event(
                EventFilter()
                .with_from_address(felt.from_hex(contract))
                .with_keys([felt.from_int(selector)])
            )

        # beast contract
        for adventurer_event in [
            "MintAdventurer",
            "UpdateAdventurerState",
            "AdventurerLeveledUp",
            "Discovery",
            "AdventurerInitiatedKingHiest",
            "AdventurerRobbedKing",
            "AdventurerDiedRobbingKing",
            "AdventurerKilledThief",
        ]:
            add_filter(config.ADVENTURER_CONTRACT, adventurer_event)

        # beast contract
        for beast_event in [
            "CreateBeast",
            "UpdateBeastState",
            "BeastLevelUp",
            "BeastAttacked",
            "AdventurerAttacked",
            "FledBeast",
            "AdventurerAmbushed",
        ]:
            add_filter(config.BEAST_CONTRACT, beast_event)

        # loot contract
        for loot_event in [
            "UpdateItemState",
            "ItemXPIncrease",
            "ItemGreatnessIncrease",
            "ItemNamePrefixesAssigned",
            "ItemNameSuffixAssigned",
            "ClaimItem",
            "ItemMerchantUpdate",
        ]:
            add_filter(config.LOOT_CONTRACT, loot_event)

        return IndexerConfiguration(
            filter=filter,
            starting_cursor=starknet_cursor(config.STARTING_BLOCK),
            finality=DataFinality.DATA_STATUS_PENDING,
        )

    async def handle_data(self, info: Info, data: Block):
        block_time = data.header.timestamp.ToDatetime()
        # Handle one block of data
        for event_with_tx in data.events:
            event = event_with_tx.event
            event_name = self.event_map[felt.to_int(event.keys[0])]
            await {
                "MintAdventurer": self.mint_adventurer,
                "UpdateAdventurerState": self.update_adventurer_state,
                "AdventurerLeveledUp": self.adventurer_level_up,
                "Discovery": self.discovery,
                "AdventurerInitiatedKingHiest": self.initiated_hiest,
                "AdventurerRobbedKing": self.robbed_king,
                "AdventurerDiedRobbingKing": self.died_robbing_king,
                "AdventurerKilledThief": self.killed_thief,
                "CreateBeast": self.create_beast,
                "UpdateBeastState": self.update_beast_state,
                "BeastLevelUp": self.beast_level_up,
                "BeastAttacked": self.beast_attacked,
                "AdventurerAttacked": self.adventurer_attacked,
                "FledBeast": self.fled_beast,
                "AdventurerAmbushed": self.adventurer_ambushed,
                "UpdateItemState": self.update_item_state,
                "ItemXPIncrease": self.item_xp_increase,
                "ItemGreatnessIncrease": self.item_greatness_increase,
                "ItemNamePrefixesAssigned": self.item_prefixes_assigned,
                "ItemNameSuffixAssigned": self.item_suffix_assigned,
                "ClaimItem": self.claim_item,
                "ItemMerchantUpdate": self.update_merchant_item,
            }[event_name](info, block_time, event.from_address, event.data)

    async def mint_adventurer(
        self,
        info: Info,
        block_time: datetime,
        _: FieldElement,
        data,
    ):
        ma = decode_mint_adventurer_event(data)
        mint_adventurer_doc = {
            "adventurer_id": check_exists_int(ma.adventurer_id),
            "owner": check_exists_int(ma.owner),
            "timestamp": block_time,
        }
        await info.storage.insert_one("adventurers", mint_adventurer_doc)
        print("- [mint adventurer]", ma.adventurer_id, "->", ma.owner)

    async def update_adventurer_state(
        self,
        info: Info,
        block_time: datetime,
        _: FieldElement,
        data,
    ):
        ua = decode_update_adventurer_state_event(data)
        update_adventurer_doc = {
            "adventurer_id": check_exists_int(ua.adventurer_id),
            "race": check_exists_int(ua.adventurer_state["Race"]),
            "home_realm": check_exists_int(ua.adventurer_state["HomeRealm"]),
            "birthdate": check_exists_int(ua.adventurer_state["Birthdate"]),
            "name": check_exists_int(ua.adventurer_state["Name"]),
            "order": check_exists_int(ua.adventurer_state["Order"]),
            "image_hash_1": check_exists_int(ua.adventurer_state["ImageHash1"]),
            "image_hash_2": check_exists_int(ua.adventurer_state["ImageHash2"]),
            "health": encode_int_as_bytes(ua.adventurer_state["Health"]),
            "level": encode_int_as_bytes(ua.adventurer_state["Level"]),
            "strength": encode_int_as_bytes(ua.adventurer_state["Strength"]),
            "dexterity": encode_int_as_bytes(ua.adventurer_state["Dexterity"]),
            "vitality": encode_int_as_bytes(ua.adventurer_state["Vitality"]),
            "intelligence": encode_int_as_bytes(ua.adventurer_state["Intelligence"]),
            "wisdom": encode_int_as_bytes(ua.adventurer_state["Wisdom"]),
            "charisma": encode_int_as_bytes(ua.adventurer_state["Charisma"]),
            "luck": encode_int_as_bytes(ua.adventurer_state["Luck"]),
            "xp": encode_int_as_bytes(ua.adventurer_state["XP"]),
            "weapon_id": check_exists_int(ua.adventurer_state["WeaponId"]),
            "chest_id": check_exists_int(ua.adventurer_state["ChestId"]),
            "head_id": check_exists_int(ua.adventurer_state["HeadId"]),
            "waist_id": check_exists_int(ua.adventurer_state["WaistId"]),
            "feet_id": check_exists_int(ua.adventurer_state["FeetId"]),
            "hands_id": check_exists_int(ua.adventurer_state["HandsId"]),
            "neck_id": check_exists_int(ua.adventurer_state["NeckId"]),
            "ring_id": check_exists_int(ua.adventurer_state["RingId"]),
            "status": check_exists_int(ua.adventurer_state["Status"]),
            "beast": check_exists_int(ua.adventurer_state["Beast"]),
            "upgrading": encode_int_as_bytes(ua.adventurer_state["Upgrading"]),
            "timestamp": block_time,
        }
        await info.storage.find_one_and_update(
            "adventurers",
            {
                "adventurer_id": encode_int_as_bytes(ua.adventurer_id),
            },
            {"$set": update_adventurer_doc},
        )
        print(
            "- [update adventurer state]", ua.adventurer_id, "->", ua.adventurer_state
        )

    async def adventurer_level_up(
        self,
        info: Info,
        block_time: datetime,
        _: FieldElement,
        data: List[FieldElement],
    ):
        pass

    async def discovery(
        self,
        info: Info,
        block_time: datetime,
        _: FieldElement,
        data: List[FieldElement],
    ):
        d = decode_discovery_event(data)
        discovery_doc = {
            "adventurer_id": check_exists_int(d.adventurer_id),
            "discovery_type": check_exists_int(d.discovery_type),
            "sub_discovery_type": check_exists_int(d.sub_discovery_type),
            "entity_id": check_exists_int(d.entity_id),
            "output_amount": encode_int_as_bytes(d.output_amount),
            "discovery_time": block_time,
        }
        await info.storage.insert_one("discoveries", discovery_doc)

    async def initiated_hiest(
        self,
        info: Info,
        block_time: datetime,
        _: FieldElement,
        data: List[FieldElement],
    ):
        ih = decode_update_adventurer_state_event(data)
        heist_doc = {
            "adventurer_id": check_exists_int(ih.adventurer_id),
            "timestamp": block_time,
        }
        await info.storage.insert_one("heists", heist_doc)

    async def robbed_king(
        self,
        info: Info,
        block_time: datetime,
        _: FieldElement,
        data: List[FieldElement],
    ):
        pass

    async def died_robbing_king(
        self,
        info: Info,
        block_time: datetime,
        _: FieldElement,
        data: List[FieldElement],
    ):
        pass

    async def killed_thief(
        self,
        info: Info,
        block_time: datetime,
        _: FieldElement,
        data: List[FieldElement],
    ):
        pass

    async def create_beast(
        self,
        info: Info,
        block_time: datetime,
        _: FieldElement,
        data: List[FieldElement],
    ):
        cb = decode_create_beast_event(data)
        beast_doc = {
            "beast_token_id": check_exists_int(cb.adventurer_id),
            "adventurer_id": check_exists_int(cb.beast_state["Adventurer"]),
            "created_date": block_time,
            "beast_type": check_exists_int(cb.beast_state["Id"]),
            "attack_type": check_exists_int(cb.beast_state["AttackType"]),
            "armor_type": check_exists_int(cb.beast_state["ArmorType"]),
            "rank": check_exists_int(cb.beast_state["Rank"]),
            "prefix_1": check_exists_int(cb.beast_state["Prefix_1"]),
            "prefix_2": check_exists_int(cb.beast_state["Prefix_2"]),
            "health": encode_int_as_bytes(cb.beast_state["Health"]),
            "xp": encode_int_as_bytes(cb.beast_state["XP"]),
            "level": encode_int_as_bytes(cb.beast_state["Level"]),
            "slain_on_date": check_exists_timestamp(cb.beast_state["SlainOnDate"]),
            "last_updated": block_time,
        }
        await info.storage.insert_one("beasts", beast_doc)

    async def update_beast_state(
        self,
        info: Info,
        block_time: datetime,
        _: FieldElement,
        data: List[FieldElement],
    ):
        ub = decode_beast_state_event(data)
        update_beast_doc = {
            "beast_id": check_exists_int(ub.beast_token_id),
            "adventurer_id": check_exists_int(ub.beast_state["Adventurer"]),
            "beast_type": check_exists_int(ub.beast_state["Id"]),
            "attack_type": check_exists_int(ub.beast_state["AttackType"]),
            "armor_type": check_exists_int(ub.beast_state["ArmorType"]),
            "rank": check_exists_int(ub.beast_state["Rank"]),
            "prefix_1": check_exists_int(ub.beast_state["Prefix_1"]),
            "prefix_2": check_exists_int(ub.beast_state["Prefix_2"]),
            "health": encode_int_as_bytes(ub.beast_state["Health"]),
            "xp": encode_int_as_bytes(ub.beast_state["XP"]),
            "level": encode_int_as_bytes(ub.beast_state["Level"]),
            "slain_on_date": check_exists_timestamp(ub.beast_state["SlainOnDate"]),
            "last_updated": block_time,
        }
        beast_state = await info.storage.find_one(
            "beasts",
            {
                "beast_id": encode_int_as_bytes(ub.beast_token_id),
            },
        )
        if beast_state:
            await info.storage.find_one_and_update(
                "beasts",
                {
                    "beast_id": encode_int_as_bytes(ub.beast_token_id),
                },
                {
                    "$set": update_beast_doc,
                },
            )
        else:
            await info.storage.insert_one(
                "beasts",
                update_beast_doc,
            )
        print("- [update beast state]", ub.beast_token_id, "->", ub.beast_state)

    async def beast_level_up(
        self,
        info: Info,
        block_time: datetime,
        _: FieldElement,
        data: List[FieldElement],
    ):
        pass

    async def beast_attacked(
        self,
        info: Info,
        block_time: datetime,
        _: FieldElement,
        data: List[FieldElement],
    ):
        ba = decode_beast_attacked_event(data)
        attacked_beast_doc = {
            "beast_token_id": check_exists_int(ba.beast_token_id),
            "adventurer_token_id": check_exists_int(ba.adventurer_token_id),
            "damage": encode_int_as_bytes(ba.damage),
            "last_updated": block_time,
        }
        battle_state = await info.storage.find_one(
            "battles",
            {
                "beast_token_id": check_exists_int(ba.beast_token_id),
                "adventurer_token_id": check_exists_int(ba.adventurer_token_id),
            },
        )
        if battle_state:
            await info.storage.find_one_and_update(
                "battles",
                {
                    "beast_token_id": check_exists_int(ba.beast_token_id),
                    "adventurer_token_id": check_exists_int(ba.adventurer_token_id),
                },
                {"$set": attacked_beast_doc},
            )
        else:
            await info.storage.insert_one("battles", attacked_beast_doc)
        print(
            "- [beast attacked]",
            ba.beast_token_id,
            "->",
            ba.adventurer_token_id,
            "-",
            ba.damage,
            "damage",
        )

    async def adventurer_attacked(
        self,
        info: Info,
        block_time: datetime,
        _: FieldElement,
        data: List[FieldElement],
    ):
        aa = decode_beast_attacked_event(data)
        attacked_adventurer_doc = {
            "beast_token_id": check_exists_int(aa.beast_token_id),
            "adventurer_token_id": check_exists_int(aa.adventurer_token_id),
            "damage": encode_int_as_bytes(aa.damage),
            "last_updated": block_time,
        }
        battle_state = await info.storage.find_one(
            "battles",
            {
                "beast_token_id": check_exists_int(aa.beast_token_id),
                "adventurer_token_id": check_exists_int(aa.adventurer_token_id),
            },
        )
        if battle_state:
            await info.storage.find_one_and_update(
                "battles",
                {
                    "beast_token_id": check_exists_int(aa.beast_token_id),
                    "adventurer_token_id": check_exists_int(aa.adventurer_token_id),
                },
                {"$set": attacked_adventurer_doc},
            )
        else:
            await info.storage.insert_one(
                "battles",
                attacked_adventurer_doc,
            )
        print(
            "- [adventurer attacked]",
            aa.adventurer_token_id,
            "->",
            aa.beast_token_id,
            "-",
            aa.damage,
            "damage",
        )

    async def fled_beast(
        self,
        info: Info,
        block_time: datetime,
        _: FieldElement,
        data: List[FieldElement],
    ):
        pass

    async def adventurer_ambushed(
        self,
        info: Info,
        block_time: datetime,
        _: FieldElement,
        data: List[FieldElement],
    ):
        pass

    async def update_item_state(
        self,
        info: Info,
        block_time: datetime,
        _: FieldElement,
        data: List[FieldElement],
    ):
        ui = decode_item_state_event(data)
        update_item_doc = {
            "market_item_id": check_exists_int(ui.market_item_id),
            "item_id": check_exists_int(ui.item_id),
            "item": check_exists_int(ui.item_state["Id"]),
            "slot": check_exists_int(ui.item_state["Slot"]),
            "type": check_exists_int(ui.item_state["Type"]),
            "material": check_exists_int(ui.item_state["Material"]),
            "rank": check_exists_int(ui.item_state["Rank"]),
            "prefix_1": check_exists_int(ui.item_state["Prefix_1"]),
            "prefix_2": check_exists_int(ui.item_state["Prefix_2"]),
            "suffix": check_exists_int(ui.item_state["Suffix"]),
            "greatness": check_exists_int(ui.item_state["Greatness"]),
            "createdBlock": check_exists_timestamp(ui.item_state["CreatedBlock"]),
            "xp": encode_int_as_bytes(ui.item_state["XP"]),
            "adventurerId": check_exists_int(ui.item_state["Adventurer"]),
            "bag": check_exists_int(ui.item_state["Bag"]),
        }
        item_state = await info.storage.find_one(
            "items",
            {
                "item_id": check_exists_int(ui.item_id),
            },
        )
        if item_state:
            await info.storage.find_one_and_update(
                "items",
                {
                    "item_id": check_exists_int(ui.item_id),
                },
                {"$set": update_item_doc},
            )
        else:
            await info.storage.insert_one(
                "items",
                update_item_doc,
            )
        print("- [update item state]", ui.item_id, "->", ui.update_item_doc)

    async def item_xp_increase(
        self,
        info: Info,
        block_time: datetime,
        _: FieldElement,
        data: List[FieldElement],
    ):
        pass

    async def item_greatness_increase(
        self,
        info: Info,
        block_time: datetime,
        _: FieldElement,
        data: List[FieldElement],
    ):
        pass

    async def item_prefixes_assigned(
        self,
        info: Info,
        block_time: datetime,
        _: FieldElement,
        data: List[FieldElement],
    ):
        pass

    async def item_suffix_assigned(
        self,
        info: Info,
        block_time: datetime,
        _: FieldElement,
        data: List[FieldElement],
    ):
        pass

    async def claim_item(
        self,
        info: Info,
        block_time: datetime,
        _: FieldElement,
        data: List[FieldElement],
    ):
        ci = decode_claim_item_event(data)
        claim_item_doc = {
            "market_item_id": check_exists_int(ci.market_item_id),
            "item_id": check_exists_int(ci.item_token_id),
            "adventurer_id": check_exists_int(ci.adventurer_token_id),
            "owner": check_exists_int(ci.owner),
            "claimed_time": block_time,
        }
        await info.storage.find_one_and_update(
            "tokens",
            {
                "market_item_id": check_exists_int(ci.market_item_id),
            },
            {
                "$set": claim_item_doc,
            },
        )
        print("- [claim item]", ci.market_item_id, "->", ci.item_token_id)
        pass

    async def update_merchant_item(
        self,
        info: Info,
        block_time: datetime,
        _: FieldElement,
        data: List[FieldElement],
    ):
        um = decode_item_merchant_update_event(data)
        update_merchant_doc = {
            "market_item_id": check_exists_int(um.market_item_id),
            "item": check_exists_int(um.item["Id"]),
            "slot": check_exists_int(um.item["Slot"]),
            "type": check_exists_int(um.item["Type"]),
            "material": check_exists_int(um.item["Material"]),
            "rank": check_exists_int(um.item["Rank"]),
            "prefix_1": check_exists_int(um.item["Prefix_1"]),
            "prefix_2": check_exists_int(um.item["Prefix_2"]),
            "suffix": check_exists_int(um.item["Suffix"]),
            "greatness": check_exists_int(um.item["Greatness"]),
            "created_block": check_exists_timestamp(um.item["CreatedBlock"]),
            "xp": encode_int_as_bytes(um.item["XP"]),
            "adventurerId": check_exists_int(um.item["Adventurer"]),
            "bag": check_exists_int(um.item["Bag"]),
            "price": check_exists_int(um.bid["price"]),
            "expiry": check_exists_timestamp(um.bid["expiry"]),
            "bidder": check_exists_int(um.bid["bidder"]),
            "status": check_exists_int(um.bid["status"]),
            "last_updated": block_time,
        }
        insert_merchant_doc = {
            "market_item_id": check_exists_int(um.market_item_id),
            "item_id": None,
            "owner": None,
            "claimed_time": None,
            "item": check_exists_int(um.item["Id"]),
            "slot": check_exists_int(um.item["Slot"]),
            "type": check_exists_int(um.item["Type"]),
            "material": check_exists_int(um.item["Material"]),
            "rank": check_exists_int(um.item["Rank"]),
            "prefix_1": check_exists_int(um.item["Prefix_1"]),
            "prefix_2": check_exists_int(um.item["Prefix_2"]),
            "suffix": check_exists_int(um.item["Suffix"]),
            "greatness": check_exists_int(um.item["Greatness"]),
            "created_block": check_exists_int(um.item["CreatedBlock"]),
            "xp": encode_int_as_bytes(um.item["XP"]),
            "adventurer_id": check_exists_int(um.item["Adventurer"]),
            "bag": check_exists_int(um.item["Bag"]),
            "price": check_exists_int(um.bid["price"]),
            "expiry": check_exists_timestamp(um.bid["expiry"]),
            "bidder": check_exists_int(um.bid["bidder"]),
            "status": check_exists_int(um.bid["status"]),
            "last_updated": block_time,
        }
        market_item = await info.storage.find_one(
            "tokens",
            {
                "market_item_id": check_exists_int(um.market_item_id),
            },
        )
        if market_item:
            await info.storage.find_one_and_update(
                "tokens",
                {
                    "market_item_id": check_exists_int(um.market_item_id),
                },
                {
                    "$set": update_merchant_doc,
                },
            )
        else:
            await info.storage.insert_one(
                "items",
                insert_merchant_doc,
            )
        print("- [update merchant item]", um.market_item_id, "->", um.bid)

    async def handle_invalidate(self, _info: Info, _cursor: Cursor):
        raise ValueError("data must be finalized")


async def run_indexer(server_url=None, mongo_url=None, restart=None):
    AUTH_TOKEN = os.environ.get("AUTH_TOKEN")
    runner = IndexerRunner(
        config=IndexerRunnerConfiguration(
            stream_url=server_url,
            storage_url=mongo_url,
            token=AUTH_TOKEN,
        ),
        reset_state=restart,
    )

    # ctx can be accessed by the callbacks in `info`.
    await runner.run(LootSurvivorIndexer(), ctx={"network": "starknet-testnet"})
