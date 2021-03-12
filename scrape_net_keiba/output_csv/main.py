import csv

element_for_predict = ["uma_number", "horse_name", "uma_nenrei", "kinryo", "jocky", "area", "trainer"]

race_data = ["scrapyで吐き出したリストを入れる"]


def export_csv(export_list):
    with open("race_data.csv", "a")as f:
        writer = csv.writer(f, lineterminator='\n')

        if isinstance(export_list[0], list):
            writer.writerows(export_list)
        else:
            writer.writerow(export_list)


export_csv(element_for_predict)
export_csv(race_data)
