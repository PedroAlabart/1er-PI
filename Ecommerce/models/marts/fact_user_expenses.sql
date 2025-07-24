SELECT 
    u.usuario_id,
    u.nombre,
    u.apellido,
    ROUND(SUM(o.total), 2) AS total_acumulado,
    ROUND(AVG(o.total), 2) AS promedio_total
FROM 
    {{ref ('stg_usuarios')}} u
INNER JOIN 
        {{ref ('stg_ordenes')}} o 
        ON u.usuario_id = o.usuario_id
GROUP BY 
    u.usuario_id, u.nombre, u.apellido
ORDER BY 
    total_acumulado DESC