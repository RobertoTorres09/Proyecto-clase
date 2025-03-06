{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "class Torniquete:\n",
    "    def __init__(self):\n",
    "        self.estado = \"Bloqueado\"\n",
    "    \n",
    "    def procesar_entrada(self,entrada):\n",
    "        if self.estado == \"Bloqueado\":\n",
    "            if entrada == 1:\n",
    "                self.estado == \"Desbloqueado\"\n",
    "                print(\"Se ha desbloqueado, puedes pasar\")\n",
    "            elif entrada == 2:\n",
    "                self.estado == \"Bloqueado\"\n",
    "                print(\"Sin efecto\")\n",
    "            else:\n",
    "                print(\"Inválido, ingrese 1 o 2 solamente\")\n",
    "        elif self.estado == \"Desbloqueado\":\n",
    "            if entrada == 1:\n",
    "                self.estado ==  \"Desbloqueado\"\n",
    "                print(\"Sin efecto\")\n",
    "            elif entrada == 2:\n",
    "                self.estado == \"Bloqueado\"\n",
    "            else:\n",
    "                print(\"Inválido, ingrese 1 o 2 solamente\")\n",
    "    \n",
    "    def ejecutar(self):\n",
    "        while True:\n",
    "            print(f\"\\nEstado actual: {self.estado}\")\n",
    "            try:\n",
    "                entrada = int(input(\"Elige una opción: 1 para Echar moneda, 2 para Empujar\"))\n",
    "                self.procesar_entrada(entrada)\n",
    "            except ValueError:\n",
    "                print(\"Por favor, ingresse un número válido\")\n",
    "\n",
    "torniquete = Torniquete()\n",
    "torniquete.ejecutar()"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": ".venv",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.13.1"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 2
}
