.PHONY: clean dev

dev:
	uvicorn main:app --reload

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -name "*.pyc" -delete
	rm -f data/yaki.db
