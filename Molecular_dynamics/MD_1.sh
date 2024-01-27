#! /bin/bash
# el script habria que ejecutarlo una vez por cada proteina y ligando ahora mismo.


# obtenemos ficheros
folders=$(find . -type d -name "*lig_*")

# cambiamos variables de ambiente para encontrar los ejecutables y usar la 2ª grafica
AMBERHOME=/usr/local/amber22
export CUDA_VISIBLE_DEVICES="1"

for f in $folders
do 
	cd $f

	# ejecutamos equilibrado y produccion en 4 partes
	echo "MINIMIZACION"
	$AMBERHOME/bin/pmemd.cuda -O -i min.in -o min.out -p complejo_h2o.parm7 -c complejo_h2o.rst7 \
	-r min.rst7 -ref complejo_h2o.rst7

	echo "CALENTADO"
	$AMBERHOME/bin/pmemd.cuda -O -i heat.in -o heat.out -p complejo_h2o.parm7 -c min.rst7 \
	-r heat.rst7 -x heat.trj -ref min.rst7

	gzip -9 heat.trj

	echo "DENSIDAD"
	$AMBERHOME/bin/pmemd.cuda -O -i density.in -o density.out -p complejo_h2o.parm7 -c heat.rst7 \
	-r density.rst7 -x density.trj -ref heat.rst7

	gzip -9 density.trj

	echo "EQUILIBRADO"
	$AMBERHOME/bin/pmemd.cuda -O -i equil.in -o equil.out -p complejo_h2o.parm7 -c density.rst7 \
	-r equil.rst7 -x equil.trj

	gzip -9 equil.trj

	echo "PROD_1"
	$AMBERHOME/bin/pmemd.cuda -O -i prod.in -o prod1.out \
	-p complejo_h2o.parm7 -c equil.rst7 -r prod1.rst7 -x prod1.trj

	echo "PROD_2"
	$AMBERHOME/bin/pmemd.cuda -O -i prod.in -o prod2.out \
	-p complejo_h2o.parm7 -c equil.rst7 -r prod2.rst7 -x prod2.trj

	echo "PROD_3"
	$AMBERHOME/bin/pmemd.cuda -O -i prod.in -o prod3.out \
	-p complejo_h2o.parm7 -c equil.rst7 -r prod3.rst7 -x prod3.trj

	echo "PROD_4"
	$AMBERHOME/bin/pmemd.cuda -O -i prod.in -o prod4.out \
	-p complejo_h2o.parm7 -c equil.rst7 -r prod4.rst7 -x prod4.trj

	echo "MMGBSA"
	$AMBERHOME/bin/MMPBSA.py -O -i mmgbsa.in -o FINAL_RESULTS_MMPBSA.dat -sp complejo_h2o.parm7 -cp complejo_gas.parm7 -rp receptor_gas.parm7 -lp ligand_gas.parm7 -y *.trj

	cd ../
done
