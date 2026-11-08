FROM rocker/r-ver:4.4.1
WORKDIR /app


# Install R packages first so this layer is cached when only main.R changes
COPY src/rscripts/install_packages.R .
RUN Rscript install_packages.R

COPY data/ data/
COPY src/rscripts/main.R .
CMD ["Rscript", "main.R"]
