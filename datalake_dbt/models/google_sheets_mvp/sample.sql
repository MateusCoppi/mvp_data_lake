{{ config(materialized='table') }}

with sheet_data as (

    select
        id,
        conta as "Conta",
        categoria as "Categoria",
        descricao as "Descrição",
        "valor__R__"::numeric(12,2) as "Valor R$",
        observacoes as "Observações",
        cast(data_transacao as date) as "Data de Transação",
        tipo_transacao as "Tipo de Transação",
        metodo_pagamento as "Método de Pagamento"
    from 
    public."Pagina1"

)

select *
from sheet_data
