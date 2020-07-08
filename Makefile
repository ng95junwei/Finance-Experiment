include .env

.PHONY:	run ingest backtest install download

run:	download ingest backtest display_results clean

ingest:
	zipline -e extension.py ingest --bundle $$BUNDLE_NAME --show-progress

backtest:
	zipline -e extension.py run -f $$ALGO_FILE --start $$START_DATE --end $$END_DATE --capital-base $$CAPITAL_BASE --bundle $$BUNDLE_NAME --trading-calendar $$TRADING_CALENDAR --benchmark-symbol $$BENCHMARK_SYMBOL -o $$RESULT_FILE

clean:
	rm -r daily

install:
	./install.sh

download: 
	python ./backtest/download.py

display_results:
	python ./backtest/display_results.py