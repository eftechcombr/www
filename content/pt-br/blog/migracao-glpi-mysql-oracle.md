---
title: "Migração do banco GLPI: de StatefulSet para MySQL na Oracle Cloud"
description: "Migramos o banco de dados do GLPI de um StatefulSet Kubernetes para instância MySQL gratuita da Oracle Cloud. Acompanhe os resultados com Grafana."
summary: "Neste final de semana migramos o banco de dados do GLPI que rodava em StatefulSet Kubernetes para o MySQL HeatWave da Oracle Cloud (Always Free). Agora o monitoramento com Grafana já está mostrando os primeiros resultados."
date: 2026-06-22
draft: false
tags: ["glpi", "mysql", "oracle-cloud", "kubernetes", "grafana", "migracao", "observabilidade"]
categories: ["infraestrutura"]
---

Neste final de semana realizamos a migração do banco de dados do GLPI — que até então operava dentro de um **StatefulSet no Kubernetes** — para o **MySQL HeatWave** da Oracle Cloud, utilizando os recursos do programa [Always Free](/pt-br/blog/oracle-always-free/).

## O cenário anterior

O GLPI da EF-TECH rodava com banco de dados em um StatefulSet Kubernetes com armazenamento persistente via PVC. Embora funcional, esse modelo trazia desafios:

- **Gerenciamento manual de backups** — sem snapshot automatizado fora do cluster
- **Consumo de recursos do cluster** — CPU e memória do banco competiam com os demais workloads
- **Manutenção do MySQL** — atualizações de versão e tuning exigiam intervenção manual nos pods
- **Alta disponibilidade limitada** — o StatefulSet com um único réplica era um ponto único de falha

## A solução: Oracle MySQL HeatWave

A Oracle Cloud oferece no programa Always Free um **DB System MySQL HeatWave** com:

- **50 GB de armazenamento** para dados
- **50 GB adicionais** para backups automatizados
- **Instância standalone** gerenciada — sem preocupação com manutenção do sistema operacional ou do MySQL
- **Backups automáticos** — retenção configurável sem custo adicional

Além disso, ao sair do cluster Kubernetes, liberamos recursos para os workloads principais e eliminamos a complexidade de operar um banco de dados stateful dentro do Kubernetes.

## O processo de migração

A migração foi planejada para causar o menor impacto possível:

1. **Provisionamento** do DB System MySQL HeatWave no OCI (região home)
2. **Exportação** do banco de dados do StatefulSet Kubernetes com `mysqldump`
3. **Importação** dos dados para a instância MySQL na Oracle Cloud
4. **Atualização da string de conexão** na aplicação GLPI (ConfigMap + variáveis de ambiente)
5. **Redirecionamento do tráfego** e validação dos dados
6. **Desativação** do StatefulSet antigo

### Comandos utilizados

Exportação dos dados do StatefulSet:

```bash
kubectl exec -n glpi deployment/glpi-mysql -- \
  mysqldump --all-databases --single-transaction --quick \
  -u root -p"$MYSQL_ROOT_PASSWORD" > glpi-backup.sql
```

Importação para o MySQL HeatWave:

```bash
mysql -h <oci-mysql-host> -u admin -p < glpi-backup.sql
```

Atualização da configuração no ConfigMap do GLPI:

```bash
kubectl edit configmap glpi-config -n glpi
# Atualizar: GLPI_DB_HOST, GLPI_DB_PORT, GLPI_DB_USER, GLPI_DB_PASSWORD
```

## Observabilidade com Grafana

Com o banco de dados agora rodando fora do cluster, aproveitamos para configurar o monitoramento via **Grafana** com métricas do MySQL HeatWave. Os principais dashboards incluem:

- **Conexões ativas** — número de conexões simultâneas com o GLPI
- **Consultas por segundo (QPS)** — volume de queries e tendências de carga
- **Tempo de resposta (latência)** — p95 e p99 das consultas mais lentas
- **Uso de armazenamento** — crescimento do banco ao longo do tempo
- **Backups** — status e retenção dos backups automáticos
- **Alertas** — notificações para conexões acima do threshold, replicação atrasada e espaço em disco

![Dashboard Grafana - MySQL HeatWave](/img/blog/glpi-mysql-grafana.png)

## Primeiros resultados

Após as primeiras horas de operação, os resultados já são positivos:

| Métrica | Antes (StatefulSet) | Depois (MySQL HeatWave) |
|---|---|---|
| Latência média de queries | ~12 ms | ~4 ms |
| Tempo de backup manual | ~25 min | Automático (zero esforço) |
| Recursos do cluster liberados | — | 2 vCPUs e 4 GB RAM |
| Manutenção do MySQL | Manual | Gerenciada pela Oracle |

## Próximos passos

Durante esta semana vamos acompanhar de perto as métricas no Grafana para:

1. Validar a estabilidade da conexão entre o GLPI (no Kubernetes) e o MySQL (no OCI)
2. Ajustar thresholds de alerta conforme a linha de base de operação
3. Avaliar a necessidade de tuning de queries específicas do GLPI
4. Documentar o processo para replicação em outros ambientes

---

Tem GLPI rodando na sua infraestrutura e quer migrar para um modelo mais sustentável? A **EF-TECH** tem experiência em planejar e executar migrações de banco de dados com segurança e mínimo downtime. [Entre em contato](/pt-br/contato/) para conversarmos.
