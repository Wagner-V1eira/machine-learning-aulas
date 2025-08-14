# 🛠️ Plano de Correções - Comandos UV

## ✅ **PROGRESSO ATUAL - 14 de Agosto 2025**

### 🎉 **CONCLUÍDO COM SUCESSO:**

**✅ Problema #1: Comandos com "Failed to canonicalize script path"** - **RESOLVIDO**
- ✅ `uv run python scripts/tasks.py fmt` - Funcionando
- ✅ `uv run python scripts/tasks.py typecheck` - Funcionando  
- ✅ `uv run python scripts/tasks.py test` - Funcionando
- **Solução:** Modificado para usar `python -m [ferramenta]`

**✅ Problema #2: Problemas de Qualidade de Código (Lint)** - **RESOLVIDO**
- ✅ `uv run python scripts/tasks.py lint` - Funcionando perfeitamente
- **Resultado:** 75 erros → 0 erros
- **Método:** 70 correções automáticas + 5 correções manuais

### ⏸️ **AINDA PENDENTE:**

**❌ Problema #3: Execução de Notebooks Falhando** - **A INVESTIGAR**
- ❌ `uv run python scripts/tasks.py run-notebooks` - Todos os 9 notebooks falharam
- **Causa:** Warnings ProactorEventLoop + problemas diversos

**⚠️ Problema #4: Erros de Tipos (typecheck)** - **FUNCIONANDO MAS COM ERROS**
- ⚠️ `uv run python scripts/tasks.py typecheck` - 15 erros de tipos
- **Causa:** Falta de stubs, tipos missing, etc.

**⚠️ Problema #5: Testes Falhando** - **FUNCIONANDO MAS COM FALHAS**
- ⚠️ `uv run python scripts/tasks.py test` - 11 testes falharam
- **Causa:** Arquivos missing, problemas de notebook format, etc.

---

## 📋 Problemas Identificados e Plano de Ação

### 🔴 **PRIORIDADE ALTA - Problemas Críticos**

#### 1. **Comandos com "Failed to canonicalize script path"**

**Status:** ❌ Não funcionam  
**Comandos afetados:**

- `uv run python scripts/tasks.py fmt`
- `uv run python scripts/tasks.py typecheck`
- `uv run python scripts/tasks.py test`

**Causa:** O UV no Windows não consegue executar diretamente os scripts `black`, `mypy`, `pytest`

**Solução:**

- [ ] Modificar `scripts/tasks.py` para usar `python -m [ferramenta]` em vez de executar diretamente
- [ ] Testar cada comando modificado
- [ ] Validar que a funcionalidade permanece a mesma

**Arquivos a modificar:**

- `scripts/tasks.py` (linhas ~83, ~94, ~104)

---

#### 2. **Problemas de Qualidade de Código (Lint)**

**Status:** ⚠️ Funciona mas encontra 75 erros  
**Comando afetado:**

- `uv run python scripts/tasks.py lint`

**Problemas encontrados:**

- 75 erros no total
- 59 podem ser corrigidos automaticamente
- Imports não utilizados
- Anotações de tipo deprecated (`typing.Dict` → `dict`)
- Problemas de estilo

**Solução:**

- [ ] Executar correções automáticas do ruff
- [ ] Corrigir problemas manuais restantes
- [ ] Verificar se lint passa sem erros

**Arquivos afetados:**

- `core/grading/api.py`
- `core/grading/result_schema.py`
- `core/grading/sandbox.py`
- `core/utils/io.py`
- `core/utils/plotting.py`
- Arquivos de testes e scripts

---

### 🟡 **PRIORIDADE MÉDIA - Problemas Funcionais**

#### 3. **Execução de Notebooks Falhando**

**Status:** ❌ Todos os 9 notebooks falharam  
**Comando afetado:**

- `uv run python scripts/tasks.py run-notebooks`

**Problemas identificados:**

- Warnings do ProactorEventLoop no Windows
- Erros de execução em todos os notebooks
- Problemas com joblib/memory mapping

**Solução:**

- [ ] Investigar logs específicos de cada notebook
- [ ] Verificar se é problema de dependências
- [ ] Testar execução individual de notebooks
- [ ] Configurar event loop adequado para Windows

**Arquivos a investigar:**

- `scripts/run_all_notebooks.py`
- Notebooks individuais em `modules/*/lessons/`

---

#### 4. **Configuração Windows/UV**

**Status:** ⚠️ Parcialmente funcionando  
**Problemas identificados:**

- Warnings sobre hardlink no UV
- Problemas de canonicalização de paths
- Possíveis incompatibilidades Windows

**Solução:**

- [ ] Configurar `UV_LINK_MODE=copy`
- [ ] Investigar configurações específicas do Windows
- [ ] Documentar workarounds necessários

---

### 🟢 **PRIORIDADE BAIXA - Melhorias**

#### 5. **Documentação e Usabilidade**

**Status:** ✅ Funcional mas pode melhorar

**Melhorias:**

- [ ] Adicionar seção de troubleshooting no README
- [ ] Documentar problemas conhecidos no Windows
- [ ] Criar script de diagnóstico
- [ ] Adicionar comandos alternativos para Windows

---

## 🎯 **Ordem de Execução Sugerida**

### **Fase 1: Correções Críticas (1-2 horas)** ✅ **CONCLUÍDA**

1. ✅ **Corrigir scripts/tasks.py** para usar `python -m` - **CONCLUÍDO**
2. ✅ **Testar comandos fmt, typecheck, test** - **CONCLUÍDO**
3. ✅ **Executar correções automáticas de lint** - **CONCLUÍDO**

### **Fase 2: Limpeza de Código (30-60 min)** ✅ **CONCLUÍDA**

4. ✅ **Corrigir problemas de lint restantes** - **CONCLUÍDO**
5. ✅ **Validar que lint passa sem erros** - **CONCLUÍDO**

### **Fase 3: Investigação Notebooks (1-2 horas)** ⏸️ **PENDENTE**

6. ⏸️ **Debuggar execução de notebooks** - **A FAZER**
7. ⏸️ **Identificar causa raiz dos erros** - **A FAZER**
8. ⏸️ **Implementar correções** - **A FAZER**

### **Fase 4: Polimento (30 min)** ⏸️ **PENDENTE**

9. ⏸️ **Configurar UV para Windows** - **A FAZER**
10. ⏸️ **Atualizar documentação** - **A FAZER**

---

## � **Próximos Passos**

**✅ CONCLUÍDO:** Comandos UV principais funcionando no Windows

**🎯 Para continuar (Fases 3-4):**
1. **Investigar falhas nos notebooks** - `run-notebooks` comando
2. **Resolver erros de tipos** - melhorar type hints e instalar stubs
3. **Corrigir testes falhando** - arquivos missing + notebook format
4. **Configurar UV otimizado para Windows** - eliminar warnings
5. **Documentar troubleshooting** - adicionar seção no README

**📊 Status Final desta Sessão:**
- ✅ 5 comandos UV funcionando perfeitamente
- ✅ 0 erros de lint (era 75)
- ✅ Código formatado e limpo
- ⚠️ 3 comandos ainda com problemas (funcionais mas com erros)

**Meta alcançada:** Comandos críticos de desenvolvimento agora funcionam! 🎉

| Comando         | Status               | Prioridade | Estimativa |
| --------------- | -------------------- | ---------- | ---------- |
| `setup`         | ✅ OK                | -          | -          |
| `install`       | ✅ OK                | -          | -          |
| `help`          | ✅ OK                | -          | -          |
| `grade`         | ✅ OK                | -          | -          |
| `clean`         | ✅ OK                | -          | -          |
| `update`        | ✅ OK                | -          | -          |
| `lint`          | ✅ OK                | ✅ Completo | ✅ Completo |
| `fmt`           | ✅ OK                | ✅ Completo | ✅ Completo |
| `typecheck`     | ⚠️ Funciona c/ erros | � Média    | 1h         |
| `test`          | ⚠️ Funciona c/ erros | � Média    | 1h         |
| `run-notebooks` | ❌ Notebooks falham  | 🟡 Média   | 2h         |

---

## 🚀 **Próximos Passos**

**Começar por:** Corrigir problema "Failed to canonicalize script path" no `scripts/tasks.py`

**Comando para testar progresso:**

```bash
uv run python scripts/tasks.py help
```

**Meta:** Ter todos os comandos UV funcionando perfeitamente no Windows
