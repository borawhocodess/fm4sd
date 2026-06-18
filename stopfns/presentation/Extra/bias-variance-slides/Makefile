.PHONY: main clean view FORCE

BUILD := build

main: $(BUILD)/bias-variance.pdf

# tectonic is the engine installed on this machine (not latexmk/lualatex).
$(BUILD)/bias-variance.pdf: bias-variance.tex FORCE | $(BUILD)
	tectonic -X compile bias-variance.tex --outdir $(BUILD)

$(BUILD):
	mkdir -p $(BUILD)

view: main
	open $(BUILD)/bias-variance.pdf

clean:
	rm -rf $(BUILD)
