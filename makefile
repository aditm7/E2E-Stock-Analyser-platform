all:
	@chmod +x scripts/*.sh
	@scripts/clean.sh
	@scripts/delete_db.sh
	@scripts/create_db.sh
	@clear
	@./scripts/run.sh

clean:
	@scripts/clean.sh
	@scripts/delete_db.sh