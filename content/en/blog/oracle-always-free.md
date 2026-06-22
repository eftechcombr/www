---
title: "Oracle Cloud Always Free: unlimited free cloud resources"
description: "Discover all Oracle Cloud Infrastructure (OCI) Always Free resources — compute, databases, storage, networking, and more, available for the lifetime of your account."
summary: "Oracle Cloud Infrastructure (OCI) offers a generous Always Free tier including AMD and ARM compute instances, autonomous databases, 200 GB of block storage, load balancers, and 10 TB of outbound data transfer per month."
date: 2026-06-19
draft: false
tags: ["oracle", "oci", "cloud-computing", "infrastructure"]
categories: ["cloud-computing"]
featureimage: "img/blog/oracle-always-free/featured.svg"
featureimagecaption: "Photo by [Oracle](https://www.oracle.com/cloud/free/)"
---

Oracle Cloud Infrastructure (OCI) provides one of the most generous **Always Free** programs among major cloud providers. Unlike trials that expire after 30 or 90 days, Always Free resources are available **for the lifetime of your account** in your tenancy's home region.

Whether you are running a personal project, building a proof of concept, or learning cloud computing, this guide covers every Always Free resource available.

## Compute

OCI offers two Always-Free compute options:

### VM.Standard.E2.1.Micro (AMD)

- **Processor:** 1/8 OCPU AMD (with burst capability)
- **Memory:** 1 GB
- **Networking:** 1 VNIC with 1 public IP, up to 50 Mbps (internet) or 480 Mbps (intra-region)
- **Images:** Oracle Linux, Oracle Linux Cloud Developer, Ubuntu, CentOS
- **Limit:** up to 2 instances per account

### VM.Standard.A1.Flex (ARM — Ampere)

- **Processor:** up to 2 OCPUs total (flexible: 1 instance with 2 OCPUs or 2 instances with 1 OCPU each)
- **Memory:** up to 12 GB total
- **Networking:** bandwidth and VNICs scale with OCPUs
- **Images:** Oracle Linux, Oracle Linux Cloud Developer, Ubuntu
- **Limit:** 1,500 OCPU hours and 9,000 GB-hours per month

> ⚠️ **Idle instances may be reclaimed.** If CPU is below 20%, network below 20%, and memory below 20% (A1 only) for 7 consecutive days, Oracle may stop the instance.

## Storage

### Block Volume

- **200 GB** total combined boot and block volumes
- **5 concurrent volume backups**
- Each instance's boot volume uses 50 GB from this pool
- Always Free volumes must be in the home region

### Object Storage

- **20 GB** combined Standard, Infrequent Access, and Archive
- **50,000 monthly** Object Storage API requests

## Database

### Oracle Autonomous AI Database

- **2 instances** Always Free per tenancy
- **1 OCPU** and **20 GB storage** each
- Supported workloads: Transaction Processing, JSON Database, APEX Application Development, Lakehouse
- **20 concurrent sessions** per database

### Oracle NoSQL Database

- Up to **133 million reads** per month
- Up to **133 million writes** per month
- **3 tables** with **25 GB** each

### Oracle MySQL HeatWave

- **1 standalone DB system** with HeatWave
- **50 GB** data storage + **50 GB** backup storage

## Networking

### Virtual Cloud Network (VCN)

- Up to **2 VCNs** per Free Tier tenancy
- IPv4 and IPv6 support

### Load Balancer

- **1 Flexible Load Balancer** (10 Mbps min/max) — tenancies created after Dec 15, 2020
- Older tenancies: 1 Micro Load Balancer (10 Mbps)
- Up to 16 listeners and 1,024 backends

### Network Load Balancer

- **1 NLB** Always Free
- Up to 50 listeners, 50 backend sets, 1,024 backends

### Site-to-Site VPN

- Up to **50 IPSec connections**

### VCN Flow Logs

- **10 GB per month** shared with Logging service

## Observability & Management

- **Monitoring:** 500 million ingestion + 1 billion retrieval data points
- **Application Performance Monitoring:** 1,000 tracing events and 10 Synthetic Monitor runs per hour
- **Connector Hub:** 2 Always Free connectors
- **Notifications:** 1 million HTTPS and 1,000 email notifications per month
- **Logging:** included, shares the 10 GB monthly pool with VCN Flow Logs
- **Console Dashboards:** 100 dashboards per tenancy
- **Email Delivery:** 3,000 emails per month
- **Fleet Application Management:** lifecycle management for the first 25 resources per month

## Security

- **Vault:** unlimited software-protected keys + 20 HSM key versions + 150 secrets
- **Bastion:** restricted, time-limited SSH access — **free** for all account types

## Additional Services

- **Certificates:** 5 CAs and 150 certificates
- **Cluster Placement Groups:** 10 to 50 per region
- **Resource Manager:** 100 stacks, 100 templates, 100 configuration source providers, 2 concurrent jobs
- **Outbound Data Transfer:** **10 TB per month** of outbound traffic

## Important Tips

1. **Home region required:** Always Free resources like block volumes and compute instances are only free in your tenancy's home region.
2. **Monitor your limits:** Go to **Governance & Administration → Limits, Quotas and Usage** in the OCI Console.
3. **Upgrade preserves Always Free:** upgrading to a paid account keeps all Always Free resources at no cost — you only pay for usage above the limits.
4. **Idle instances get reclaimed:** keep your instances active to avoid losing them.
5. **Use Resource Manager for quick provisioning:** OCI templates can deploy a full Always Free stack in minutes via Terraform.

## Conclusion

The Oracle Cloud Always Free tier is an excellent choice for personal projects, learning labs, and proof-of-concept work. With AMD and ARM compute instances, autonomous databases, 200 GB of storage, and 10 TB of monthly data transfer, you have enough resources to run real applications without worrying about costs.

At **EF-TECH**, we have hands-on experience with Oracle Cloud projects and can help your company plan and execute OCI migrations focused on cost savings and best practices. [Get in touch](/en/contato/) to learn more.
