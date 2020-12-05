select a.name, a.born, a.birthplace, a.description, count(q.author_name) from author a inner join quotes q on q.author_name = a.name
group by a.name

select * from quotes