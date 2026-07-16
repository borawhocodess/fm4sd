.PHONY: main clean FORCE

BUILD := build

main: $(BUILD)/rdbbench.pdf

$(BUILD)/rdbbench.pdf: rdbbench.tex FORCE | $(BUILD)
	latexmk -quiet -outdir=$(BUILD) -pdflatex='lualatex -interaction nonstopmode' -pdf rdbbench.tex

$(BUILD):
	mkdir -p $(BUILD)

clean:
	latexmk -outdir=$(BUILD) -pdf -C
	rm -rf $(BUILD)
