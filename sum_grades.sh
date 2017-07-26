#!/bin/bash
notas_recebidas=$(sed -n 's/.*(\(.*\) de \(.*\)).*/\1/p' $1)
notas_maximas=$(sed -n 's/.*(\(.*\) de \(.*\)).*/\2/p' $1)
somaNotas=0; notaMaxima=0
#TODO se houver algum "de" em texto no arquivo, vai dar crash
for i in $notas_recebidas; do somaNotas=$(echo $somaNotas + $i | bc); done
for i in $notas_maximas;   do notaMaxima=$(echo $notaMaxima + $i | bc); done

echo "Nota do aluno: $somaNotas de $notaMaxima"