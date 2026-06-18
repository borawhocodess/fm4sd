.PHONY: main clean view FORCE

BUILD := build

main: $(BUILD)/classification-trees.pdf

# tectonic is the engine installed on this machine (not latexmk/lualatex).
$(BUILD)/classification-trees.pdf: classification-trees.tex FORCE | $(BUILD)
	tectonic -X compile classification-trees.tex --outdir $(BUILD)

$(BUILD):
	mkdir -p $(BUILD)

view: main
	open $(BUILD)/classification-trees.pdf

clean:
	rm -rf $(BUILD)
