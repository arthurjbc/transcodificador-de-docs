````markdown
# Documento de Teste de Transcodificação Markdown → HTML

> Este documento foi gerado para testes de desempenho, concorrência e consumo de memória.

---

# Sumário

1. Introdução
2. Objetivos
3. Estrutura
4. Listas
5. Tabelas
6. Código
7. Citações
8. Imagens
9. Links
10. Seções Repetidas

---

# Introdução

Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum commodo, magna sed elementum tincidunt, erat lectus fermentum mauris, sed vulputate ipsum purus vel justo.

Lorem ipsum dolor sit amet, consectetur adipiscing elit. Suspendisse potenti. Integer feugiat justo sed erat gravida, non pellentesque odio condimentum.

---

# Objetivos

- Testar parser Markdown
- Testar geração de HTML
- Testar concorrência
- Testar uso de memória
- Testar tempo de CPU
- Testar cache
- Testar renderização

---

# Lista Numerada

1. Item 1
2. Item 2
3. Item 3
4. Item 4
5. Item 5
6. Item 6
7. Item 7
8. Item 8
9. Item 9
10. Item 10

---

# Lista Não Ordenada

- Alpha
- Bravo
- Charlie
- Delta
- Echo
- Foxtrot
- Golf
- Hotel
- India
- Juliet
- Kilo
- Lima
- Mike
- November
- Oscar
- Papa
- Quebec
- Romeo
- Sierra
- Tango
- Uniform
- Victor
- Whiskey
- X-Ray
- Yankee
- Zulu

---

# Tabela

| ID | Nome | Valor | Status |
|----|------|-------|--------|
| 1 | Produto A | 10 | OK |
| 2 | Produto B | 20 | OK |
| 3 | Produto C | 30 | Erro |
| 4 | Produto D | 40 | OK |
| 5 | Produto E | 50 | Processando |
| 6 | Produto F | 60 | OK |
| 7 | Produto G | 70 | OK |
| 8 | Produto H | 80 | Falhou |
| 9 | Produto I | 90 | OK |
|10 | Produto J |100 | OK |

---

# Código Go

```go
package main

import "fmt"

func fibonacci(n int) int {
    if n < 2 {
        return n
    }
    return fibonacci(n-1) + fibonacci(n-2)
}

func main() {
    for i := 0; i < 20; i++ {
        fmt.Println(i, fibonacci(i))
    }
}
````

---

# Código Java

```java
public class Main {

    public static long factorial(long n) {
        if (n <= 1) return 1;
        return n * factorial(n - 1);
    }

    public static void main(String[] args) {
        for(int i=1;i<=20;i++){
            System.out.println(i + " -> " + factorial(i));
        }
    }
}
```

---

# Código Python

```python
def primes(limit):
    result = []
    for n in range(2, limit):
        prime = True
        for i in range(2, int(n**0.5)+1):
            if n % i == 0:
                prime = False
                break
        if prime:
            result.append(n)
    return result

print(primes(100))
```

---

# Citação

> Lorem ipsum dolor sit amet, consectetur adipiscing elit.
>
> Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.

---

# Links

* https://example.com
* https://github.com
* https://golang.org
* https://python.org

---

# Imagem

![Imagem](https://picsum.photos/800/400)

---

# Texto Longo

Lorem ipsum dolor sit amet, consectetur adipiscing elit.

Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla facilisi. Donec euismod, ligula eget posuere suscipit, metus nulla egestas ligula, vitae commodo odio lacus vitae nisi.

Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec in mauris sed sapien tincidunt viverra.

Lorem ipsum dolor sit amet, consectetur adipiscing elit. Integer pretium purus vel mauris consequat, vel bibendum lectus vulputate.

---

# Seções Repetidas

```
Repita o bloco abaixo 100 vezes para aumentar significativamente o tamanho do documento.
```

## Bloco X

### Cabeçalho

Lorem ipsum dolor sit amet, consectetur adipiscing elit.

* item A
* item B
* item C
* item D
* item E

| Campo | Valor |
| ----- | ----- |
| A     | 100   |
| B     | 200   |
| C     | 300   |
| D     | 400   |
| E     | 500   |

```json
{
  "id": 12345,
  "name": "Documento",
  "active": true,
  "items": [
    1,2,3,4,5,6,7,8,9,10
  ]
}
```

Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed vitae justo sit amet velit vulputate elementum. Suspendisse potenti. Integer facilisis tortor sit amet ipsum luctus, ac gravida orci posuere.

Lorem ipsum dolor sit amet, consectetur adipiscing elit.

Lorem ipsum dolor sit amet, consectetur adipiscing elit.

Lorem ipsum dolor sit amet, consectetur adipiscing elit.

Lorem ipsum dolor sit amet, consectetur adipiscing elit.

---

## Bloco X+1

(repita exatamente a mesma estrutura acima)

---

## Bloco X+2

(repita exatamente a mesma estrutura acima)

---

...

Repita até chegar em aproximadamente 100 blocos.

---

# Conclusão

Este documento contém:

* centenas de cabeçalhos
* milhares de linhas
* listas
* tabelas
* blocos de código
* citações
* imagens
* links
* texto contínuo

Seu objetivo é produzir uma carga significativa para serviços de transcodificação Markdown → HTML, permitindo testes de throughput, paralelismo, consumo de memória e tempo de CPU.

```
```
