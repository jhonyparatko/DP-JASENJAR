drop table if exists lag cascade;

create table lag 
(lag int not null);
insert into lag values
(-5),(-4),(-3),(-2),(-1),(0),(1),(2),(3),(4),(5);

drop view if exists lag_correlants;

create view lag_correlants as
 select name, date, country, value, (date + lag) as lag_date, lag
  from
 t_correlants cross join  lag;

DROP VIEW if exists tfr_fact;

create view tfr_fact as 
 SELECT t_fertility_rate.country,
    t_fertility_rate.date,
    tfr,
    lag_correlants.value,
    lag_correlants.name,
    lag_correlants.lag
   FROM t_fertility_rate
     JOIN lag_correlants ON t_fertility_rate.country::text = lag_correlants.country::text 
     AND t_fertility_rate.date = lag_correlants.lag_date;

DROP VIEW if exists location_dim;

create view location_dim as
 SELECT t_country.country,
    t_country.region,
    t_country.incomegroup
   FROM t_country;