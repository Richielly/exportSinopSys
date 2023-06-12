import datetime
class Util:

    def increment_seconds_on_duplicates(self, data, datetime_column):
        seen = {}
        new_data = []

        for line in data:
            elements = line.strip().split('|')
            date_str = elements[datetime_column]
            date_obj = datetime.datetime.strptime(date_str, "%d/%m/%Y %H:%M:%S")

            while date_obj in seen:
                date_obj += datetime.timedelta(seconds=1)

            seen[date_obj] = True
            elements[datetime_column] = date_obj.strftime("%d/%m/%Y %H:%M:%S")
            new_data.append('|'.join(elements))

        return new_data

    def process_file(self, file_path, datetime_column):
        with open(file_path, 'r') as file:
            data = file.readlines()

        new_data = self.increment_seconds_on_duplicates(data, datetime_column)

        with open(file_path, 'w') as file:
            file.writelines('\n'.join(new_data))


util = Util()
util.process_file(r'D:\Conversao\Acacia\410\Arquivos\Processados\Acumulador.txt', 3)