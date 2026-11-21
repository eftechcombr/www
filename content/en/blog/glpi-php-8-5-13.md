---
title: "GLPI: Base Image Updated to PHP 8.5.13"
description: "EF-TECH's GLPI container distribution updates its PHP-FPM base image to PHP 8.5.13 and zlib 1.4."
summary: "The Docker base image used by the GLPI distribution was upgraded from PHP 8.5.12 to PHP 8.5.13, with zlib updated to 1.4-r0 on Alpine 3.24. The change keeps GLPI at 12.0.2 and does not alter the application image versions."
date: 2026-11-21
draft: false
tags: ["glpi", "docker", "php", "infrastructure"]
categories: ["infrastructure"]
---

The PHP base image for [EF-TECH's GLPI distribution](https://github.com/eftechcombr/glpi) has been updated to **PHP 8.5.13**, replacing version 8.5.12. The change was published in the repository on November 21, 2026.

## What changed

The update is in `docker/php/Dockerfile.base` and includes:

- The base image changed from `php:8.5.12-fpm-alpine3.24` to `php:8.5.13-fpm-alpine3.24`.
- The `zlib-dev` development package changed from `1.3.2-r1` to `1.4-r0`, matching the version available in Alpine 3.24.

This base image provides the PHP-FPM environment used to build the application image. The change does not update the GLPI application itself: its configured version remains **GLPI 12.0.2**. The Nginx version was not changed either.

## What to do when updating

Users of the published images should check the available tags in the [releases repository](https://github.com/eftechcombr/glpi/releases) and follow their usual deployment update process. If you build the images locally, rebuild the PHP-FPM image to incorporate the new base.

Before applying updates in production, keep backups of the database and GLPI files current, and validate the deployment in a staging environment.

## References

- [EF-TECH GLPI repository](https://github.com/eftechcombr/glpi)
- [PHP 8.5.13 base image update](https://github.com/eftechcombr/glpi/commit/80a94b030b60eb0f4f69a9ff2273433d96d6ca0b)
- [EF-TECH GLPI product](/en/produtos/glpi/)
