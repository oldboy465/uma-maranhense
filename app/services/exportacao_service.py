import io
import csv

class ExportacaoService:
    @staticmethod
    def gerar_csv(colunas, linhas):
        """
        Gera um arquivo CSV compativel com o Excel no Brasil (delimitador ';', UTF-8 com BOM).
        Formata valores numericos e monetarios com vírgula para casas decimais.
        """
        output = io.StringIO()
        # UTF-8 BOM para garantir correta abertura de acentos no Excel Windows
        output.write('\ufeff')
        
        writer = csv.writer(output, delimiter=';', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(colunas)

        for linha in linhas:
            linha_formatada = []
            for item in linha:
                if item is None:
                    linha_formatada.append('')
                elif isinstance(item, float):
                    item_arr = round(item, 2)
                    linha_formatada.append(str(item_arr).replace('.', ','))
                else:
                    linha_formatada.append(str(item))
            writer.writerow(linha_formatada)

        output.seek(0)
        return output.getvalue().encode('utf-8')