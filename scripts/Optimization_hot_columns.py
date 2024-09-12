import ROOT
import numpy as np
from astropy.io import fits
import matplotlib.pyplot as plt


# Cargo la data, pedestal substracted y la mask, los cluster enmascarados
data_image = fits.getdata("/home/perez/Downloads/composed_fits_data_Amp2.fits")

print(np.logical_not(data_image).sum())
clusters = fits.getdata(
    "/home/perez/Downloads/composed_fits_mask_Amp2.fits").astype(bool)

one_three_electron_mask = np.logical_not(
    np.logical_and(data_image > 0.75, data_image < 3.25))

initial_mask = np.logical_or(clusters, one_three_electron_mask)

# mask0 = combination.mask.copy()

one_electron = 0.75
three_electron = 3.25
one_three_electrons = np.zeros((np.shape(data_image)))
'''
for entry in tree:
    for pixel_e in entry.pixels_E:
        if pixel_e >= one_electron and pixel_e <= three_electron:
            one_three_electrons[entry.pixels_x, entry.pixels_y] = 1
        else:
            one_three_electrons[entry.pixels_x, entry.pixels_y] = 0

# Ahora voy enmascarando aquellas columnas que superen cierto sigma
sigma_ch = 30  # Este es el sigma más alto que vamos a tapar


# print("La combinación de los datos es: \n", combination[240:250, 480:500])
# Densidad de eventos con energía entre 1 e y 3 e
print("La cantidad de eventos con energía entre 1 e y 3 e es: ",
      np.sum(one_three_electrons))
print("El número de pixeles no enmascarados es: ", np.sum(~mascara))

print("La densidad de eventos con energía entre 1 e y 3 e es: ",
      np.sum(one_three_electrons)/np.sum(~mascara))

print("El número de pixeles no enmascarados es: ",
      np.sum(~combination.mask.astype(bool)))
print("El número de pixeles enmascarados es: ",
      np.sum(combination.mask.astype(bool)))
'''
# Cargamos el archivo con las columnas y sus sigmas
columnas_sigma = np.loadtxt(
    "/home/perez/Downloads/all_columns_sigma.txt", dtype=float, skiprows=1)

densidad = []
sigmas = []
eve_1_3_ele = []
# Este es el sigma más alto que vamos a tapar
# sigma_ch = np.linspace(30, 2, 18)
sigma_ch = 30

for sigma in range(sigma_ch, 1, -1):
    # Calculo la nueva mascara
    mask0 = initial_mask.copy()
    new_mask = np.zeros((np.shape(data_image)))
    Ncols_ini = np.shape(data_image)[1]
    # Columnas que superan el sigma
    columnas_con_sigma_mayor = columnas_sigma[abs(
        columnas_sigma[:, 1]) > sigma][:, 0]
    # Convertir columnas_con_sigma_mayor a un array de NumPy con valores enteros
    columnas_con_sigma_mayor = columnas_con_sigma_mayor.astype(int)
    print(
        f"Las columnas que superan el sigma de {sigma} son: {columnas_con_sigma_mayor}")
    Ncols_mask = len(columnas_con_sigma_mayor)
    # new_mask enmascara las columnas con sigma mayor
    mask0[:, columnas_con_sigma_mayor] = True
    eve_1_3_ele.append(np.logical_not(mask0).sum())
    # print("La cantidad de eventos con energía entre 1 e y 3 e es: ", eve_1_3_ele[-1])
    # Densidad de eventos con energía entre 1 e y 3 e
  #  eve_tot = np.sum(~(combination_sigma.mask.astype(bool)))
   # print("El número de pixeles no enmascarados es: ", eve_tot)
    densidad.append(eve_1_3_ele[-1]/(Ncols_ini - Ncols_mask))
    sigmas.append(sigma)
    # input("Presione Enter para continuar...")
# Plotear la densidad frente a las sigmas
plt.plot(30 - np.array(sigmas), densidad)

# Donde está el minimo de densidad
min_index = np.argmin(densidad)
# Plotear el minimo con un punto rojo
plt.plot(30 - sigmas[min_index], densidad[min_index], "ro")

plt.xlabel("$30$ - Sigma", fontsize=18)
# In latex
plt.ylabel("$\\rho$ of events between 1 $e^{-}$ and 3 $e^{-}$", fontsize=18)
# plt.title("Density of events between 1 $e^{-}$ and 3 $e^{-}$ vs Sigma")
plt.legend(["$\\rho$ of events between 1 $e^{-}$ and 3 $e^{-}$",
           f"Minimum, sigma = {sigmas[min_index]}"], fontsize=18)

# Ajustar el tamaño de la fuente de los valores de los ejes
plt.tick_params(axis='both', which='major', labelsize=16)
plt.tick_params(axis='both', which='minor', labelsize=16)

image_name = "/home/perez/Downloads/density_vs_sigma.png"
plt.savefig(image_name)
print(f"El gráfico se ha guardado como {image_name}.")

plt.show()
