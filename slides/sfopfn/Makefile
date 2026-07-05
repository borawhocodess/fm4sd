.PHONY: main clean FORCE

BUILD := build

main: $(BUILD)/sfopfn.pdf

$(BUILD)/sfopfn.pdf: sfopfn.tex FORCE | $(BUILD)
	latexmk -quiet -outdir=$(BUILD) -pdflatex='lualatex -interaction nonstopmode' -pdf sfopfn.tex

$(BUILD):
	mkdir -p $(BUILD)

clean:
	latexmk -outdir=$(BUILD) -pdf -C
	rm -rf $(BUILD)
