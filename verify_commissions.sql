-- Verificar estado de comisiones y órdenes

-- 1. Verificar usuarios con volúmenes
SELECT 
    member_id, 
    first_name, 
    last_name,
    pv_cache, 
    pvg_cache, 
    vn_cache,
    status
FROM users 
ORDER BY member_id;

-- 2. Verificar órdenes completadas
SELECT 
    id,
    buyer_member_id,
    total_amount,
    currency,
    status,
    created_at
FROM orders 
WHERE status = 'completed'
ORDER BY created_at DESC;

-- 3. Verificar comisiones registradas
SELECT 
    id,
    member_id,
    bonus_type,
    amount_converted,
    currency_destination,
    status,
    period_id,
    calculated_at
FROM commissions 
ORDER BY calculated_at DESC;

-- 4. Verificar billeteras
SELECT 
    member_id,
    balance,
    currency,
    status
FROM wallets 
ORDER BY member_id;

-- 5. Verificar transacciones de wallet
SELECT 
    member_id,
    transaction_type,
    amount,
    currency,
    status,
    created_at
FROM wallet_transactions 
ORDER BY created_at DESC;

-- 6. Verificar períodos
SELECT 
    id,
    name,
    starts_on,
    ends_on,
    closed_at
FROM periods 
ORDER BY starts_on DESC;
