import ROOT
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import os


# Open the files
file2 = ROOT.TFile("/home/perez/Downloads/combined_Amp_2.root")
file3 = ROOT.TFile("/home/perez/Downloads/combined_Amp_3.root")

# Espera entrada del usuario
Amp = input("What amplifier do you want to analyze? (2/3): ")

while True:
    if Amp == "2":
        file = file2
        break
    elif Amp == "3":
        file = file3
        break
    else:
        print("Invalid amplifier. Please enter 2 or 3.")
        Amp = input("What amplifier do you want to analyze? (2/3): ")
'''
# Draw the dark current vs file number
h2 = ROOT.TH2F(
    "h2", f"Dark current vs the File number of the Amplifier {Amp}", 120, 0.5, 120.5, 110, 0, 0.3)
h2.SetStats(True)
h2.SetXTitle("File number")
h2.SetYTitle("Dark current (e-)")
h2.SetMarkerStyle(20)  # Estilo de marcador: redondo
h2.SetMarkerColor(ROOT.kBlack)  # Color del marcador:
file.info.Draw(f"{Amp}_dc:nfile>>h2")
ROOT.gPad.Update()
input("Presiona Enter para continuar...")  # Espera entrada del usuario

# Draw the gain vs file number
h3 = ROOT.TH2F(
    "h3", f"Gain vs the File number of the Amplifier {Amp}", 120, 0.5, 120.5, 110, 210, 240)
file.info.Draw(f"{Amp}_gain:nfile>>h3")
'''
'''
# Create histograms to see the hot columns and rows
histx = ROOT.TH1F("histx", "Pixels in columns", 3100, 0.5, 3100.5)
histx.SetStats(True)
histx.SetXTitle("Column")
histx.SetYTitle("# Counts")
histx.SetMarkerStyle(20)  # Estilo de marcador: redondo
histx.SetMarkerColor(ROOT.kBlack)  # Color del marcador:
'''
histy = ROOT.TH1F("histy", "Pixels in rows", 500, 0.5, 500.5)
histy.SetStats(True)
histy.SetXTitle("Row")
histy.SetYTitle("# Counts")
histy.SetMarkerStyle(20)  # Estilo de marcador: redondo
histy.SetMarkerColor(ROOT.kBlack)  # Color del marcador:
'''
# Fill the histograms
file.clustersRec.Draw("pixels_x>>histx", "!has_seed")
input("Presiona Enter para continuar...")  # Espera entrada del usuario
'''

file.clustersRec.Draw("pixels_y>>histy", "!has_seed")
input("Presiona Enter para continuar...")  # Espera entrada del usuario

# Calculate the mean and the standard deviation of the histograms excluding the extreme values
# meanx = trim_mean(histx, 0.1, 0.9)

# Datos de ejemplo
# a = [1, 1, 1, 1, 1, 1, 1, 1, 9, 10]

# Calcular los percentiles del 10% y 90%
lower_bound = np.percentile(histy, 10)
upper_bound = np.percentile(histy, 90)


# Calcular la desviación estándar truncada
tstd_value = stats.tstd(histy, limits=(lower_bound, upper_bound))

# Imprimir los resultados
print("Percentil 10%:", lower_bound)
print("Percentil 90%:", upper_bound)
print("Desviación estándar truncada:", tstd_value)
'''
# Crear el histograma de los datos originales
plt.hist(histy, bins=1000, alpha=0.75,
         edgecolor='black', label='Datos originales')

# Añadir líneas verticales para los percentiles
plt.axvline(lower_bound, color='r', linestyle='dashed',
            linewidth=2, label='Percentil 10%')
plt.axvline(upper_bound, color='b', linestyle='dashed',
            linewidth=2, label='Percentil 90%')

# Añadir leyenda
plt.legend()

# Añadir títulos y etiquetas
plt.title('Distribución de Datos con Percentiles')
plt.xlabel('Valores')
plt.ylabel('Frecuencia')
plt.yscale('log')
# Rago de x automaático
plt.xlim(0, 500)

# Mostrar el gráfico
plt.show()
#plt.savefig('/home/perez/Downloads/histogram_with_percentiles.png')
#print("El gráfico se ha guardado como 'histogram_with_percentiles.png'.")
input("Presiona Enter para continuar...")  # Espera entrada del usuario
'''
'''
# Busquemos las hot rows
sigma = 4
hot_rows = []
sigma_hot_rows = []
is_hot_row = False

# Fiteamos los histogramas anteriores a una pol1 excluyendo inicio
col_ini = 20
col_fin = 3072
fit_fun = ROOT.TF1("fit_fun", "pol1", col_ini, col_fin)
histy.Fit(fit_fun, "", "", col_ini, col_fin)
p0 = fit_fun.GetParameter(0)
p1 = fit_fun.GetParameter(1)

for i in range(histy.GetNbinsX()):
    if abs(histy.GetBinContent(i) - p0 - p1*i) > sigma*tstd_value:
        is_hot_columns = True
        sigma_out = (histy.GetBinContent(i) - p0 - p1*i)/tstd_value
        sigma_hot_rows.append(sigma_out)
        hot_rows.append(i)

histy.Draw()

line_upper_fun = ROOT.TF1(
    "line_upper_fun", f"[0] + [1]*x + {sigma * tstd_value}", col_ini, col_fin)
line_upper_fun.SetParameter(0, p0)
line_upper_fun.SetParameter(1, p1)
line_upper_fun.SetLineColor(ROOT.kRed)
line_upper_fun.SetLineStyle(2)
line_upper_fun.Draw("same")

line_lower_fun = ROOT.TF1(
    "line_lower_fun", f"[0] + [1]*x - {sigma * tstd_value}", col_ini, col_fin)
line_lower_fun.SetParameter(0, p0)
line_lower_fun.SetParameter(1, p1)
line_lower_fun.SetLineColor(ROOT.kRed)
line_lower_fun.SetLineStyle(2)
line_lower_fun.Draw("same")

input("Presiona Enter para continuar...")  # Espera entrada del usuario
'''
'''
# Printeamos las hot columns
print("Hot columns: ", hot_rows)
for i in range(len(hot_rows)):
    if abs(sigma_hot_rows[i]) - sigma < 1:
        print(
            f"The column {hot_rows[i]} its:{sigma_hot_rows[i]} sigmas away from the mean. Decide yourself if it is a hot column.\n")
print("Number of hot columns: ", len(hot_rows))

# Crear un archivo de texto
# Obtener la ruta del directorio actual
current_directory = os.path.dirname(os.path.abspath(__file__))

file_name = os.path.join(current_directory, "hot_rows_sigma.txt")
with open(file_name, "w") as file:
    # Encabezado
    file.write("Hot rows".ljust(12) + "Sigma\n")

    # Escribir los datos de las hot columns y sus sigmas
    for i in range(len(hot_rows)):
        hot_row_str = str(hot_rows[i]).ljust(12)
        sigma_str = str(sigma_hot_rows[i])
        file.write(hot_row_str + sigma_str + "\n")

# Imprimir mensaje de confirmación
print(f"Se ha creado el archivo '{file_name}' con éxito.")


# Ordenar las columnas calientes
hot_rows.sort()

# Función para agrupar las columnas consecutivas


def group_consecutive(lst):
    ranges = []
    for i in lst:
        if not ranges or i > ranges[-1][-1] + 1:
            ranges.append([i])
        else:
            ranges[-1].append(i)
    return ranges


# Agrupar las columnas consecutivas
grouped_columns = group_consecutive(hot_rows)

# Lista para almacenar los grupos extendidos
extended_groups = []

# Ampliar el rango si hay más de 5 columnas consecutivas
final_ranges = []
for group in grouped_columns:
    if len(group) > 5:
        extended_range = [group[0] - 3, group[-1] + 3]
        # Ajustar el límite inferior si es negativo
        extended_range[0] = max(0, extended_range[0])
        final_ranges.append(extended_range)
        extended_groups.append(group)
    else:
        final_ranges.append([group[0], group[-1]])

# Imprimir el formato deseado
print("Grupos de columnas calientes agrupadas:")
for idx, rng in enumerate(final_ranges):
    if rng[0] == rng[-1]:
        print(f"[{rng[0]}]", end=",")
    else:
        print(f"[{rng[0]},{rng[1]}]", end=",")

# Imprimir los grupos extendidos
if extended_groups:
    print("\n\nLos siguientes grupos de columnas se han extendido:")
    for group in extended_groups:
        print(f"Grupo extendido: {group}")
'''
'''
# Fill the histograms en el mismo canvas
file.clustersRec.Draw("pixels_x>>histx2", "!has_seed && pixels_E > 0.75 && pixels_E < 1.25")
file.clustersRec.Draw(
    "pixels_x>>histx3", "!has_seed && pixels_E > 1.75*1000/3.74 && pixels_E < 2.25*1000/3.74")

# Añadir leyenda en ROOT
'''
