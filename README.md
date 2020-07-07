# Finance Experiment

This project provides an easy way to set up backtesting. This allows developers to quickly prototype algorithms and choose which stocks they want to run their prototypes against.

This project runs on `zipline` and assumes the user is using a mac and has `conda` installed.

## Installation
```bash
make install
```

## Running 
```bash
make
```
This command downloads the required data using `yahoofinancials` package and cleans it. The data is then ingested by the zipline framework and the backtesting is run. The data is then deleted from the filesystem.

If for any reason you need the individual steps, the make recipes are
`make download`

`make ingest`

`make backtest`

`make clean`