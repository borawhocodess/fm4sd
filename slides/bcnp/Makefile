.PHONY: main clean FORCE

BUILD := build

main: $(BUILD)/bcnp.pdf

$(BUILD)/bcnp.pdf: bcnp.tex FORCE | $(BUILD)
	latexmk -quiet -outdir=$(BUILD) -pdflatex='lualatex -interaction nonstopmode' -pdf bcnp.tex

$(BUILD):
	mkdir -p $(BUILD)

clean:
	latexmk -outdir=$(BUILD) -pdf -C
	rm -rf $(BUILD)
