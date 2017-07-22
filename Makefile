.PHONY: build install dist srpm rpm pypi clean

PYTHON        ?= python3
INSTALL_FLAGS ?=

NAME          := trelloment

build:
	$(PYTHON) setup.py build

install:
	id -u $(NAME) &>/dev/null || useradd -M -s /sbin/nologin $(NAME)

	mkdir -p /etc/$(NAME) /var/log/$(NAME) /opt/$(NAME) \
		&& chown $(SUDO_USER):$(SUDO_USER) /etc/$(NAME) \
		&& chown $(SUDO_USER):$(SUDO_USER) /var/log/$(NAME) \
		&& chown $(SUDO_USER):$(SUDO_USER) /opt/$(NAME)

	if [ $$(ls /etc/$(NAME) | wc -l) -eq "0" ]; then \
		cp etc/* /etc/$(NAME)/ && chown -R $(SUDO_USER):$(SUDO_USER) /etc/$(NAME); \
	fi

	$(PYTHON) setup.py install --skip-build $(INSTALL_FLAGS)

dist: clean
	$(PYTHON) setup.py sdist
	mv dist/$(NAME)-*.tar.gz .

clean:
	rm -rf build dist $(NAME)-*.tar.gz $(NAME).egg-info

remove:
	rm -rf /opt/$(NAME) /etc/$(NAME) /var/log/$(NAME)
