import os
from scipy import stats
import ROOT
import numpy as np
from astropy.io import fits
import matplotlib.pyplot as plt


ROOT.gStyle.SetOptStat(0)  # No imprimir estadísticas
# Cargo la data, pedestal substracted y la mask, los cluster enmascarados
data_image = fits.getdata("/home/perez/Downloads/composed_fits_data_Amp2.fits")
val = []
ener_3 = 0
ini = 511

for i in range(0, ini):
    val.append(data_image[ini-i, 164])
    if data_image[ini-i, 164] >= 4.75:
        ener_3 += 1
    elif data_image[ini-i, 164] <= 1.75:
        print(ini-i)
        break


print(max(val))
print(np.mean(val))
print(ener_3)


# Open the files
file2 = ROOT.TFile("/home/perez/Downloads/combined_Amp_2.root")
file3 = ROOT.TFile("/home/perez/Downloads/combined_Amp_3.root")

histogram2 = ROOT.TH1F("Histogram Amplifier 2",
                       "", 3100, 0.5, 3100.5)
file2.clustersRec.Draw("pixels_x>>Histogram Amplifier 2", "!has_seed")

histogram2.SetXTitle("Columns")
histogram2.SetYTitle("Events")

input("Press Enter to continue...")

histogram3 = ROOT.TH1F("Histogram Amplifier 3",
                       "", 3100, 0.5, 3100.5)
file3.clustersRec.Draw("pixels_x>>Histogram Amplifier 3", "!has_seed")

histogram3.SetXTitle("Columns")
histogram3.SetYTitle("Events")

input("Press Enter to continue...")

'''
# Search for peaks using TSpectrum
spectrum = ROOT.TSpectrum()
n_peaks = spectrum.Search(histogram2, 2, "goff", 0.1)
peaks = spectrum.GetPositionX()

# Plot the histogram and the peaks
c1 = ROOT.TCanvas("c1", "c1", 800, 600)
histogram2.Draw()
for i in range(n_peaks):
    line = ROOT.TLine(peaks[i], 0, peaks[i], histogram2.GetMaximum())
    line.SetLineColor(ROOT.kRed)
    line.Draw()
c1.Update()
input("Press Enter to continue...")
'''

# Calcular los percentiles del 10% y 90%
lower_bound = np.percentile(histogram2, 10)
upper_bound = np.percentile(histogram2, 90)


# Calcular la desviación estándar truncada
tstd_value = stats.tstd(histogram2, limits=(lower_bound, upper_bound))

# Quitamos el prescan

col_ini = 10
col_fin = 0
for bin in range(1, histogram2.GetNbinsX() + 1):
    if histogram2.GetBinContent(bin) != 0:
        col_fin = bin

# Cuantas columnas iniciales quitar
fit_fun_ini = ROOT.TF1("fit_fun", "pol1", col_ini, col_fin)
histogram2.Fit(fit_fun_ini, "", "", col_ini, col_fin)
p0 = fit_fun_ini.GetParameter(0)
p1 = fit_fun_ini.GetParameter(1)

vec_col_ini = []
print("el tst_value es: ", tstd_value)
for i in range(100):
    if (histogram2.GetBinContent(i) - (p0 + p1*i)) < -1.5*tstd_value:
        vec_col_ini.append(i)
print(vec_col_ini)

for i in range(2, len(vec_col_ini)):
    print(vec_col_ini[-i], vec_col_ini[-1-i], vec_col_ini[-2-i])
    if vec_col_ini[-i] - vec_col_ini[-(i+1)] <= 3 and vec_col_ini[-(i+1)] - vec_col_ini[-(i+2)] <= 3:
        col_ini = max(vec_col_ini[-i],
                      vec_col_ini[-(i+1)], vec_col_ini[-(i+2)])
        break

print("La columna inicial es: ", col_ini)


# Ahora si que podemos buscar las hot columns
sigma = 4
hot_columns = []
sigma_hot_columns = []
is_hot_columns = False

# Fiteamos los histogramas anteriores a una pol1 excluyendo inicio
# col_ini = 20
col_fin = 0
for bin in range(1, histogram2.GetNbinsX() + 1):
    if histogram2.GetBinContent(bin) != 0:
        col_fin = bin
print("La columna final es: ", col_fin)

fit_fun = ROOT.TF1("fit_fun", "pol1", col_ini, col_fin)
histogram2.Fit(fit_fun, "", "", col_ini, col_fin)
p0 = fit_fun.GetParameter(0)
p1 = fit_fun.GetParameter(1)

for i in range(histogram2.GetNbinsX()):
    if abs(histogram2.GetBinContent(i) - p0 - p1*i) > sigma*tstd_value:
        is_hot_columns = True
        sigma_out = (histogram2.GetBinContent(i) - p0 - p1*i)/tstd_value
        sigma_hot_columns.append(sigma_out)
        hot_columns.append(i)

histogram2.Draw()

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

# Añadir leyenda
legend = ROOT.TLegend(0.1, 0.75, 0.35, 0.9)
legend.AddEntry(histogram2, "Histogram of amplifier 2", "l")
legend.AddEntry(fit_fun, f"Pol1 fit", "l")
legend.AddEntry(line_upper_fun, f"Pol1 $\pm${sigma}$\sigma$", "l")
legend.Draw()

input("Presiona Enter para continuar...")  # Espera entrada del usuario


# Para el histograma 3
# Busquemos las hot columns
sigma = 4
hot_columns = []
sigma_hot_columns = []
is_hot_columns = False

# Fiteamos los histogramas anteriores a una pol1 excluyendo inicio
# col_ini = 20
# col_fin = 3072
fit_fun = ROOT.TF1("fit_fun", "pol1", col_ini, col_fin)
histogram3.Fit(fit_fun, "", "", col_ini, col_fin)
p0 = fit_fun.GetParameter(0)
p1 = fit_fun.GetParameter(1)

for i in range(histogram3.GetNbinsX()):
    if abs(histogram3.GetBinContent(i) - p0 - p1*i) > sigma*tstd_value:
        is_hot_columns = True
        sigma_out = (histogram3.GetBinContent(i) - p0 - p1*i)/tstd_value
        sigma_hot_columns.append(sigma_out)
        hot_columns.append(i)

histogram3.Draw()

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

# Añadir leyenda
legend = ROOT.TLegend(0.1, 0.75, 0.35, 0.9)
legend.AddEntry(histogram3, "Histogram of amplifier 3", "l")
legend.AddEntry(fit_fun, f"Pol1 fit", "l")
legend.AddEntry(line_upper_fun, f"Pol1 $\pm${sigma}$\sigma$", "l")
legend.Draw()

input("Presiona Enter para continuar...")  # Espera entrada del usuario
