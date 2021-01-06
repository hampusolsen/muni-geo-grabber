import xlsxwriter

current_row = 2
NAME_COLUMN = "A"
LAT_COLUMN = "B"
LNG_COLUMN = "C"

workbook = xlsxwriter.Workbook("data/Kommuners_Koordinater.xlsx", {
    'constant_memory': True
})
worksheet = workbook.add_worksheet()

worksheet.write(f"{NAME_COLUMN}1", "name")
worksheet.write(f"{LAT_COLUMN}1", "lat")
worksheet.write(f"{LNG_COLUMN}1", "lng")

def write_to_file(name, lat, lng):
    global current_row

    worksheet.write(f"{NAME_COLUMN}{current_row}", name)
    worksheet.write(f"{LAT_COLUMN}{current_row}", lat)
    worksheet.write(f"{LNG_COLUMN}{current_row}", lng)

    current_row += 1


def save_file():
    workbook.close()
