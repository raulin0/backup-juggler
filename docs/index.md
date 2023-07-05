# Backup Juggler
Backup Juggler is a command-line tool that allows you to perform multiple copies of files and directories simultaneously. The whole application is based on a command called `{{ commands.run }}`. This command has a subcommand related to each action that the application can perform. Like `do-backups` and `get-size`.

{% include "templates/cards.html" %}

{% include "templates/instalation.md" %}

## How to use?
### Using `do-backups`
You can call `do-backups` via command line. For example:

```bash
{{ commands.run }} do-backups --source <source_path> --destination <destination_directory>
```

- `--source` or `-s` option specifies the source path(s) to be backed up;
- `--destination` or `-d` option specifies the destination directory(s) for the backups.

The sources can be individual files, where the copy will be saved in a newly created directory inside the target directory, using the same name as the file; or entire directories, where the entire source directory will be copied recursively to the target directory.

!!! warning "About the sources"
    The `FileNotFoundError` exception will be raised if the paths specified as sources do not exist, so make sure you enter the paths correctly.

#### Making multiple backups
Both options can be called multiple times, allowing  the specification of multiple source paths and multiple destination directories for the backups.

1. Single source to multiple destinations
```bash
{{ commands.run }} do-backups --source '/path/to/source' --destination '/path/to/destination1' --destination '/path/to/destination2'
```
2. Multiple sources to a single destination
```bash
{{ commands.run }} do-backups --source '/path/to/source1' --source '/path/to/source2' --destination '/path/to/destination'
```
3. Multiple sources to multiple destinations
```bash
{{ commands.run }} do-backups --source '/path/to/source1' --source '/path/to/source2' --destination '/path/to/destination1' --destination '/path/to/destination2'
```

### Using `get-size`
You can call `get-size` via command line. For example:

```bash
{{ commands.run }} get-size --source <source_path>
```

- `--source` or `-s` option specifies the source path(s) that will have their total sizes calculated.

To calculate the total size of the specified source(s), which can be individual files or entire directories, where the calculation will be done recursively

!!! warning "About the sources"
    The `FileNotFoundError` exception will be raised if the paths specified as sources do not exist, so make sure you enter the paths correctly.

#### Calculating from multiple sources
The `--source` of `-s` option can be called multiple times, allowing  the specification of multiple source paths to return the sum of their total sizes

```bash
{{ commands.run }} get-size --source /path/to/source1 --source /path/to/source2
```

### More information about the CLI
The information about the command-line tool can be accessed using the `--help` flag:

```bash
{{ commands.run }} --help
```

or just

```bash
{{ commands.run }}
```
```bash
 Usage: {{ commands.run }} [OPTIONS] COMMAND [ARGS]...

 Multiple copies of files and directories simultaneously made easy.

╭─ Options ──────────────────────────────────────────────────────────────────────────────────╮
│ --version             -v        Shows the version of the Backup Juggler.                   │
│ --install-completion            Install completion for the current shell.                  │
│ --show-completion               Show completion for the current shell, to copy it or       │
│                                 customize the installation.                                │
│ --help                          Show this message and exit.                                │
╰────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ─────────────────────────────────────────────────────────────────────────────────╮
│ do-backups        Perform backups of source to destination.                                │
│ get-size          Calculate the total size of the specified source.                        │
╰────────────────────────────────────────────────────────────────────────────────────────────╯
```

### More information about subcommands
The information about subcommands also can be accessed using the `--help` flag after the parameter name. An example of using help in `do-backups`:

```bash
{{ commands.run }} do-backups --help
```
```bash
 Usage: {{ commands.run }} do-backups [OPTIONS]

 Perform backups of source to destination.

╭─ Options ──────────────────────────────────────────────────────────────────────────────────╮
│ *  --source       -s      PATH  Source path(s) to be backed up. [default: None] [required] │
│ *  --destination  -d      PATH  Destination directory(s) for the backups. [default: None]  │
│                                 [required]                                                 │
│    --help                       Show this message and exit.                                │
╰────────────────────────────────────────────────────────────────────────────────────────────╯
```