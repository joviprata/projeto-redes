# Projeto de Redes: Simulação de rede em domínio autônomo


<p align="center">
  <img src="https://github.com/user-attachments/assets/6ccec9c9-e3d4-4caa-b9c4-5984590a6889" width="50%">
</p>



## Sobre o projeto
Este projeto foi desenvolvido com o intuito de aprofundar os conceitos relativos à camada de rede e camada de enlace através de projeto de rede e simulação. 

Em [projeto_redes.py](./projeto_redes.py) está todo o código que cria uma rede em topologia de árvore a partir do documento [exemplo_de_input.txt](./exemplo_de_input.txt). Após a execução é criada uma imagem do grafo que representa a rede, uma tabela de roteamento e uma tabela de ping, ambos no formato .csv.

## Instruções de uso para executar o Projeto
É necessário a instalação das seguintes bibliotecas:
- <a href="https://matplotlib.org/stable/users/getting_started/">Matplotlib</a>
- <a href="https://networkx.org/documentation/stable/install.html">Networkx</a>
- <a href="https://pandas.pydata.org/docs/getting_started/install.html">Pandas</a>
- <a href="https://docs.python.org/3/library/collections.html">Collection</a>
### Pré-requisitos:
<a href="https://www.python.org/downloads/">python3</a>

Para rodar o projeto adequadamente é necessário fazer uma etapa inicial de criação de ambiente virtual do python:
- **Unix**:
  ```bash
  python3 -m venv .venv
  ```

- **Windows**:
  ```bash
  py -m venv .venv
  ```

Em seguida, é necessário que o ambiente virtual seja inicializado:

- **Unix**:
  ```bash
  source .venv/bin/activate
  ```

- **Windows**:
  ```bash
  .venv\Scripts\activate
  ```

Finalmente, é necessário realizar o processo de instalação das bibliotecas citadas anteriormente. Para isso, a forma mais rápida seria digitando no terminal ```pip install NOME-DA-BIBLIOTECA```.

Assim, basta rodar o código em uma IDE ou terminal. Caso apresente algum erro, recomenda-se a reinicialização da IDE utilizada para execução.


Para mais informações sobre ambientes virtuais em python, acesso o site a seguir:

<a href="https://packaging.python.org/pt-br/latest/guides/installing-using-pip-and-virtual-environments/#create-and-use-virtual-environments">https://packaging.python.org/pt-br/latest/guides/installing-using-pip-and-virtual-environments/#create-and-use-virtual-environments</a>

## Equipe

<table>
  <tr>
    <td align="center"><a href="https://github.com/joviprata"><img style="border-radius: 50%;" src="https://avatars.githubusercontent.com/u/115483518?v=4" width="100px;" alt=""/><br /><sub><b>João Victor Prata</b></sub></a><br />
      <td align="center"><a href="https://github.com/lbritors"><img style="border-radius: 50%;" src="https://avatars.githubusercontent.com/u/90286379?v=4" width="100px;" alt=""/><br /><sub><b>Leticia Brito</b></sub></a><br />
        <td align="center"><a href="https://github.com/RafaBonach"><img style="border-radius: 50%;" src="https://avatars.githubusercontent.com/u/104152350?v=4" width="100px;" alt=""/><br /><sub><b>Rafael Bonach</b></sub></a><br />  
  </tr>
</table>
