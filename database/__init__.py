# Alembic models package

# Import all models so they're available for migrations
from .addresses import Addresses, Countries
from .auth_credentials import AuthCredentials
from .comissions import Commissions
from .exchange_rates import ExchangeRates
from .orders import Orders, OrderStatus
from .order_items import OrderItems
from .periods import Periods
from .products import Products, ProductType, ProductPresentation
from .ranks import Ranks
from .roles_users import RolesUsers
from .roles import Roles
from .social_accounts import SocialAccounts, SocialNetwork
from .user_rank_history import UserRankHistory
from .userprofiles import UserProfiles, UserGender
from .users_addresses import UserAddresses
from .users import Users, UserStatus
from .usertreepaths import UserTreePath

# ✅ Nuevos modelos: Wallet, Cashback, Loyalty y Travel Points
from .wallet import Wallets, WalletTransactions, WalletWithdrawals, WalletStatus, WalletTransactionType, WalletTransactionStatus, WithdrawalStatus
from .cashback import Cashback, CashbackUsage, CashbackStatus
from .loyalty_points import LoyaltyPoints, LoyaltyPointsHistory, LoyaltyRewards, LoyaltyStatus, LoyaltyEventType, RewardType, RewardStatus
from .travel_campaigns import TravelCampaigns, NNTravelPoints, NNTravelPointsHistory, CampaignStatus, TravelEventType

# Inicialización de base de datos
from .db_init import initialize_database

__all__ = [
    "Addresses", "Countries",
    "AuthCredentials",
    "Ranks",
    "Roles",
    "RolesUsers",
    "SocialAccounts", "SocialNetwork",
    "UserProfiles", "UserGender",
    "Users", "UserStatus",
    "UserAddresses",
    "UserRankHistory",
    "UserTreePath",
    "Periods",
    "Products", "ProductType", "ProductPresentation",
    "Commissions",
    "ExchangeRates",
    "Orders", "OrderStatus",
    "OrderItems",
    # Wallet system
    "Wallets", "WalletTransactions", "WalletWithdrawals",
    "WalletStatus", "WalletTransactionType", "WalletTransactionStatus", "WithdrawalStatus",
    # Cashback system
    "Cashback", "CashbackUsage", "CashbackStatus",
    # Loyalty points system
    "LoyaltyPoints", "LoyaltyPointsHistory", "LoyaltyRewards",
    "LoyaltyStatus", "LoyaltyEventType", "RewardType", "RewardStatus",
    # Travel campaigns system
    "TravelCampaigns", "NNTravelPoints", "NNTravelPointsHistory",
    "CampaignStatus", "TravelEventType"
]