include .env

.PHONY:	run ingest backtest install download

run:	download ingest backtest clean

ingest:
	zipline ingest --bundle $$BUNDLE_NAME

backtest:
	zipline run -f $$ALGO_FILE --start $$START_DATE --end $$END_DATE --capital-base $$CAPITAL_BASE --bundle $$BUNDLE_NAME --trading-calendar $$TRADING_CALENDAR --benchmark-symbol $$BENCHMARK_SYMBOL

clean:
	rm -r daily

install:
	./install.sh

download: 
	python ./backtest/download.py
	