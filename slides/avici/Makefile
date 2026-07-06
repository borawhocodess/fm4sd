.PHONY: main clean FORCE

BUILD := build

main: $(BUILD)/avici.pdf

$(BUILD)/avici.pdf: avici.tex FORCE | $(BUILD)
	latexmk -quiet -outdir=$(BUILD) -pdflatex='lualatex -interaction nonstopmode' -pdf avici.tex

$(BUILD):
	mkdir -p $(BUILD)

clean:
	latexmk -outdir=$(BUILD) -pdf -C
	rm -rf $(BUILD)
