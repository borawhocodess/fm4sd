.PHONY: main clean view FORCE

BUILD := build

main: $(BUILD)/specific-pfns.pdf

# tectonic is the engine installed on this machine (not latexmk/lualatex).
$(BUILD)/specific-pfns.pdf: specific-pfns.tex FORCE | $(BUILD)
	tectonic -X compile specific-pfns.tex --outdir $(BUILD)

$(BUILD):
	mkdir -p $(BUILD)

view: main
	open $(BUILD)/specific-pfns.pdf

clean:
	rm -rf $(BUILD)
