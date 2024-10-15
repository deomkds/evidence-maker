# Gerador de PDF de Evidências

### O que é isso?

Na Validação de Sistemas Computadorizados, é comum coletarmos capturas de telas dos testes realizados para evidênciar os resultados encontrados durante a execução do roteiro de testes. No entanto, algumas pessoas preferem que as evidências sejam organizadas em um PDF fácil de compartilhar (e de imprimir, se você for desses).

Este script faz exatamente isso: ele é capaz de gerar um PDF com duas capturas de tela por página, inserindo nome, logotipo e número de páginas automaticamente.

### Bugs?

Sim, vários.
1. Às vezes, os números de página não batem.
2. Imagens em proporções diferentes de 16:9 podem sobrepor os textos.
3. O script é incapaz de ordenar certos tipos de numeração corretamente (1.1, 1.1.1, 1.2.1 por exemplo).

### Dependências

Necessita do [Pillow](https://pypi.org/project/pillow/).
