# Web Scraper OLX
Extração de dados do site OLX com Selenium / Scrapy. Projeto feito a partir da ideia de criar um chatbot que envia diariamente novos produtos lançados na plataforma e também para comparar a performance do Selenium ou Scrapy.

### Conclusão sobre usar Selenium ou Scrapy
Pode-se observar uma grande diferença em performance. O Selenium, por simular um browser, **é muito mais lento**, mas a vantagem é que ele pode **interagir com o JavaScript e executar outras ações que o Scrapy não consegue**. Se os dados já estiverem lá, sem precisar executar alguma ação no JavaScript, **o Scrapy é muito melhor em velocidade**. 

Mas porquê não combinar os dois? Você pode utilizar o Selenium para selecionar alguns elementos que só consegue interagindo na página e passá-los para o Scrapy extrair.

### Como usar
Acesse o [site da OLX](https://www.olx.com.br), pesquise algo, pegue a URL e coloque-a no **arquivo url.txt**

Após instalar o programa (próximo item), abra o terminal e execute o arquivo com o comando `python main.py`. Por padrão, extrairá os dados com o Scrapy, mas você pode testar o Selenium descomentando as linhas de código no arquivo main.py.

Veja os produtos extraídos no arquivo **extracted_products.json**

### Instalação
1. [Instale o Python](https://www.python.org/downloads/), se ainda não tem.

2. Abra um terminal e clone o repositório<br>
`git clone https://github.com/theervilha/Web-Scraper-OLX.git`

3. Entre na pasta e instale as bibliotecas do Python no terminal:<br>
`pip install -r requirements.txt`