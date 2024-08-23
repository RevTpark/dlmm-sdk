from dataclasses import dataclass
from enum import Enum
from solders.pubkey import Pubkey
from typing import Any, List, TypedDict

class StrategyType(Enum):
    SpotOneSide="SpotOneSide",
    CurveOneSide="CurveOneSide",
    BidAskOneSide="BidAskOneSide",
    SpotImBalanced="SpotImBalanced",
    CurveImBalanced="CurveImBalanced",
    BidAskImBalanced="BidAskImBalanced",
    SpotBalanced="SpotBalanced",
    CurveBalanced="CurveBalanced",
    BidAskBalanced="BidAskBalanced"

    def __str__(self) -> str:
        return self.name
    
    def __repr__(self) -> str:
        return self.name

class PositionVersion(Enum):
    V1="V1",
    V2="V2"

    def __str__(self) -> str:
        return self.name
    
    def __repr__(self) -> str:
        return self.name

class StrategyParameters(TypedDict):
    max_bin_id: int
    min_bin_id: int
    strategy_type: StrategyType

@dataclass
class ActiveBin():
    bin_id: int
    x_amount: str
    y_amount: str
    supply: str
    price: float
    version: int
    price_per_token: str

    def __init__(self, data: dict):
        self.bin_id = data["binId"]
        self.x_amount = data["xAmount"]
        self.y_amount = data["yAmount"]
        self.supply = data["supply"]
        self.price = float(data["price"])
        self.version = data["version"]
        self.price_per_token = data["pricePerToken"]

@dataclass
class PositionBinData():
    bin_id: int
    price: str
    price_per_token: str
    bin_x_Amount: str
    bin_y_Amount: str
    bin_liquidity: str
    position_liquidity: str
    position_x_amount: str
    position_y_amount: str

    def __init__(self, data: dict):
        self.bin_id = data["binId"]
        self.price = data["price"]
        self.price_per_token = data["pricePerToken"]
        self.bin_x_Amount = data["binXAmount"]
        self.bin_y_Amount = data["binYAmount"]
        self.bin_liquidity = data["binLiquidity"]
        self.position_liquidity = data["positionLiquidity"]
        self.position_x_amount = data["positionXAmount"]
        self.position_y_amount = data["positionYAmount"]

    def to_json(self) -> dict:
        return {
            "binId": self.bin_id,
            "price": self.price,
            "pricePerToken": self.price_per_token,
            "binXAmount": self.bin_x_Amount,
            "binYAmount": self.bin_y_Amount,
            "binLiquidity": self.bin_liquidity,
            "positionLiquidity": self.position_liquidity,
            "positionXAmount": self.position_x_amount,
            "positionYAmount": self.position_y_amount
        }

@dataclass
class PositionData():
    total_x_amount: str
    total_y_amount: str
    position_bin_data: List[PositionBinData]
    last_updated_at: int
    upper_bin_id: int
    lower_bin_id: int
    fee_X: int
    fee_Y: int
    reward_one: int
    reward_two: int
    fee_owner: str
    total_claimed_fee_X_amount: int
    total_claimed_fee_Y_amount: int

    def __init__(self, data: dict):
        self.total_x_amount = data["totalXAmount"]
        self.total_y_amount = data["totalYAmount"]
        self.position_bin_data = [PositionBinData(bin_data) for bin_data in data["positionBinData"]]
        self.last_updated_at = data["lastUpdatedAt"]
        self.upper_bin_id = data["upperBinId"]
        self.lower_bin_id = data["lowerBinId"]
        self.fee_X = data["feeX"]
        self.fee_Y = data["feeY"]
        self.reward_one = data["rewardOne"]
        self.reward_two = data["rewardTwo"]
        self.fee_owner = data["feeOwner"]
        self.total_claimed_fee_X_amount = data["totalClaimedFeeXAmount"]
        self.total_claimed_fee_Y_amount = data["totalClaimedFeeYAmount"]
    
    def to_json(self) -> dict:
        return {
            "totalXAmount": self.total_x_amount,
            "totalYAmount": self.total_y_amount,
            "positionBinData": [bin_data.to_json() for bin_data in self.position_bin_data],
            "lastUpdatedAt": self.last_updated_at,
            "upperBinId": self.upper_bin_id,
            "lowerBinId": self.lower_bin_id,
            "feeX": self.fee_X,
            "feeY": self.fee_Y,
            "rewardOne": self.reward_one,
            "rewardTwo": self.reward_two,
            "feeOwner": self.fee_owner,
            "totalClaimedFeeXAmount": self.total_claimed_fee_X_amount,
            "totalClaimedFeeYAmount": self.total_claimed_fee_Y_amount
        }

@dataclass
class Position():
    public_key: Pubkey
    position_data: PositionData
    position_version: PositionVersion

    def __init__(self, data: dict):
        self.public_key = Pubkey.from_string(data["publicKey"])
        self.position_data = PositionData(data["positionData"])
        self.position_version = data["version"]
    
    def to_json(self):
        return {
            "publicKey": str(self.public_key),
            "positionData": self.position_data.to_json(),
            "version": str(self.position_version)
        }

@dataclass
class GetPositionByUser():
    active_bin: ActiveBin
    user_positions: List[Position]

    def __init__(self, data: dict):
        self.active_bin = ActiveBin(data["activeBin"])
        self.user_positions = [Position(position) for position in data["userPositions"]]

@dataclass
class SwapQuote():
    consumed_in_amount: int
    out_amount: int
    fee: int
    protocol_fee: int
    min_out_amount: int
    price_impact: float
    bin_arrays_pubkey: List[Pubkey]

    def __init__(self, data: dict):
        self.consumed_in_amount = int(data["consumedInAmount"])
        self.out_amount = int(data["outAmount"])
        self.fee = int(data["fee"])
        self.protocol_fee = int(data["protocolFee"])
        self.min_out_amount = int(data["minOutAmount"])
        self.price_impact = float(data["priceImpact"])
        self.bin_arrays_pubkey = list(map(lambda x: Pubkey.from_string(x), data["binArraysPubkey"]))

class LBPair:
    bump_seed: List[int]
    bin_step_seed: List[int]
    pair_type: int
    active_id: int
    bin_step: int
    status: int
    require_base_factor_seed: int
    base_factor_seed: List[int]
    token_x_mint: str
    token_y_mint: str
    padding1: List[int]
    padding2: List[int]
    fee_owner: Pubkey
    base_key: str

    def __init__(self, data: dict) -> None:
        self.bump_seed = data["bumpSeed"]
        self.bin_step_seed = data["binStepSeed"]
        self.pair_type = data["pairType"]
        self.active_id = data["activeId"]
        self.bin_step = data["binStep"]
        self.status = data["status"]
        self.require_base_factor_seed = data["requireBaseFactorSeed"]
        self.base_factor_seed = data["baseFactorSeed"]
        self.token_x_mint = data["tokenXMint"]
        self.token_y_mint = data["tokenYMint"]
        self.padding1 = data["padding1"]
        self.padding2 = data["padding2"]
        self.fee_owner = Pubkey.from_string(data["feeOwner"])
        self.base_key = data["baseKey"]
        
@dataclass
class TokenReserve():
    public_key: Pubkey
    reserve: Pubkey
    amount: str
    decimal: int

    def __init__(self, data: dict) -> None:
        self.public_key = Pubkey.from_string(data["publicKey"])
        self.reserve = Pubkey.from_string(data["reserve"])
        self.amount = data["amount"]
        self.decimal = data["decimal"]

@dataclass
class PositionInfo():
    public_key: Pubkey
    lb_pair: Any
    token_x: TokenReserve
    token_y: TokenReserve
    lb_pair_positions_data: List[Position]

    def __init__(self, data: dict) -> None:
        self.public_key = Pubkey.from_string(data["publicKey"])
        self.lb_pair = data["lbPair"]
        self.token_x = TokenReserve(data["tokenX"])
        self.token_y = TokenReserve(data["tokenY"])
        self.lb_pair_positions_data = [Position(position) for position in data["lbPairPositionsData"]]

@dataclass
class FeeInfo():
    base_fee_rate_percentage: float
    max_fee_rate_percentage: float
    protocol_fee_percentage: float

    def __init__(self, data: dict) -> None:
        self.base_fee_rate_percentage = float(data["baseFeeRatePercentage"])
        self.max_fee_rate_percentage = float(data["maxFeeRatePercentage"])
        self.protocol_fee_percentage = float(data["protocolFeePercentage"])
