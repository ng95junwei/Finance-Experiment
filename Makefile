include .env

.PHONY:	run ingest backtest install download

run:	ingest backtest

ingest:
	zipline ingest --bundle $$BUNDLE_NAME

backtest:
	zipline run -f $$ALGO_FILE --start $$START_DATE --end $$END_DATE --capital-base $$CAPITAL_BASE --bundle $$BUNDLE_NAME --trading-calendar $$TRADING_CALENDAR --benchmark-symbol $$BENCHMARK_SYMBOL

install:
	./install.sh

download: 
	python ./backtest/download.py
	