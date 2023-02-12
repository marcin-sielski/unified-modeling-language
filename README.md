# Unified Modeling Language

This repository in playground for UML.

## Update Ubuntu/Debian system

```bash
sudo apt update
```

```bash
sudo apt upgrade
```

## Install UML tools under Ubuntu/Debian

* Visual Studio Code

```bash
wget https://go.microsoft.com/fwlink/?LinkID=760868 -O code-amd64.deb

```

```bash
sudo apt install ./code-amd64.deb
```

* diagrams.net

```bash
wget https://github.com/jgraph/drawio-desktop/releases/download/v20.8.16/drawio-amd64-20.8.16.deb -O drawio-amd64.deb
```

```bash
sudo apt install drawio-amd64.deb
```

## Download repository and run oven example model

```bash
git clone https://github.com/marcin-sielski/unified-modeling-language.git
```

```bash
cd unified-modeling-language
python3 oven/src/oven.py
```

## Documentation

* ![Oven UML diagrams](https://github.com/marcin-sielski/unified-modeling-language/oven/doc/oven.drawio.png)
* ![Oven UML class diagrams](https://github.com/marcin-sielski/unified-modeling-language/oven/doc/classes.oven.png)
