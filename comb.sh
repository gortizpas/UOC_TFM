#! /bin/bash
# despues de guardar cada parte del fichero de visualizacion de pymol como una molecula por separado,
# lo que hace es asignar un nuevo identificador y numero a la molecula, para luego poder crear un solo
# fichero con pymol que pueda interpretar correctamente PLIP.

# para los pasos con pymol es:
# exportar molecula -> todas -> escribir conexiones -> un documento por molecula
# ejecutar este script
# cargar moleculas en pymol (la proteina en ultimo lugar)-> exportar todas como un unico fichero -> escribir conexiones
# lo de la proteina parece que hay que hacerlo por algo del orden de los aminoacidos/ligandos, si no, PLIP no lo interpreta bien.


# me detecta lso ligandos, pero no estan bien construidos, me da a mi que por las conexiones.

files=$(find . -name "*lig*")
i=1

for f in $files
do
	new_file=$(echo $f | sed 's/.\///' | sed 's/-.*//')
        if [ $i -le 9 ]
        then

                while IFS= read -r line
                do
                echo "$line" | sed 's/UNL     1/LIG     '"$i"'/' >> $new_file.pdb
                done < "$f"
                let "i+=1"
        else
                while IFS= read -r line
                do
                echo "$line" | sed 's/UNL     1/LIG    '"$i"'/' >> $new_file.pdb
                done < "$f"
                let "i+=1"
        fi

done

rm *-*

# esta parte no hace falta, ya que PLIP no lo interpreta bien, 
# pero si se guarda un unico documento luego con Pymol, si lo consigue.

#ligands=$(find . -name "*lig_*")

#for l in $ligands
#do
#	grep "HETATM" $l >> all_ligands.pdb
#done

#protein=$(find . -name "*mod*")

#cat all_ligands.pdb >> all_complex.pdb
#cat $protein >> all_complex.pdb

