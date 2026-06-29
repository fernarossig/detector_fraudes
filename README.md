# detector_fraudes
Detector de fraudes usando Python e base de dados pronta (inspirado no método ClearSale).

Um detector de fraudes simples, usando Streamlit e Pandas, com auxílio da IA para montagem da interface inspirada num e-mail real.

O sistema se baseia em 3 níveis: nível verde (0 a 40 pontos, a compra é aprovada), amarelo (41 a 70, verificação manual por parte do comprador) e vermelho (71 a 100, compra e cartão bloqueados). O sistema lê a informações inseridas no momento da compra, como número do cartão, localização, hora, dispositivo e ticket (há uma média destas informações armazenadas). A cada informação fora da média, é somado um valor. Por exemplo: dispositivo diferente do habitual? +20. Valor muito acima da média? +40. fora do horário de costume? +20. Estes valores são somados a cada diferença detectada. Levando em conta que o brasileiro costuma ter diferentes cartões com diferentes costumes.
