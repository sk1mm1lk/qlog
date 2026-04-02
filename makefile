.PHONY: clean dev

dev:
	$(MAKE) -C yaki-server dev

clean:
	$(MAKE) -C yaki-server clean
