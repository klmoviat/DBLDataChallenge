import sqlite3
# programma om de average sentiment te krijgen van een conversatie
# misschien nutteloos: je zou ook nog alle tweets van klm weg moeten halen
# je kan van langere conversaties eventueel een plot halen van hoe het sentiment tijdens
# een conversatie veranderd, maar wat is het nut en is de software accuraat genoeg?
# en wat zegt een average sentiment van 1 conversatie? niets toch?
# misschien als je de avg sentiment van alle tweets richting een company pakt dat het nuttiger is?
# idk is verwarrend


conn = sqlite3.connect("D:\\EXPORT\\ALL_DATA.sqlite")
cursor = conn.cursor()

comp=input('company name')
conv_name = comp + '_full_conv'
cursor.execute("""create table temp_replies as
    select """ + conv_name + """.temp_head, """ + conv_name + """.tail_id, """ + comp + """.CONV_ID
    from """ + conv_name + """
inner join """ + comp + """ on """ + comp + """.tail_id = """ + conv_name + """.tail_id
order by CONV_ID;""")
cursor.execute("""create table text as select main.text, temp_replies.CONV_ID
from main
inner join temp_replies on temp_replies.temp_head = main.id_str
union
select main.text, temp_replies.CONV_ID
from main
inner join temp_replies on temp_replies.tail_id = main.id_str
order by CONV_ID asc;""")
# cursor.execute("select max(CONV_ID) from temp_replies").fetchone()[0]

for x in range(1,10):
    lst = cursor.execute("select text from text where CONV_ID = ?", (x,)).fetchall()
    true_lst = [i[0] for i in lst]
    sent=[]
    for z in range(0,len(true_lst)):
        sent_temp=evaluate(true_lst[z])) #evalueer hier de tweet, en sla 1 eindscore op? ofzo?
        sent=sent.append(sent_temp)
    average = mean(sent) #calculate average sentiment over conversation

cursor.execute("drop table text;")
cursor.execute("drop table temp_replies;")
