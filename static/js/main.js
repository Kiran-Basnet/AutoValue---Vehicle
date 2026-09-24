document.addEventListener("DOMContentLoaded", function () {

    function setupAutocomplete(
        inputId,
        suggestionsId,
        field,
        extraParams = () => ({})
    ) {
        const input = document.getElementById(inputId);
        const suggestionsBox = document.getElementById(suggestionsId);

        if (!input || !suggestionsBox) {
            return;
        }

        let requestCounter = 0;

        async function loadSuggestions(query = "") {

            const requestId = ++requestCounter;

            suggestionsBox.innerHTML = "";

            const params = new URLSearchParams({
                field: field,
                q: query,
                ...extraParams()
            });

            try {

                const response = await fetch(
                    `/api/vehicle-suggestions/?${params.toString()}`
                );

                if (!response.ok) {
                    throw new Error(
                        `HTTP error: ${response.status}`
                    );
                }

                const data = await response.json();

                // Ignore an older request if a newer one has finished
                if (requestId !== requestCounter) {
                    return;
                }

                if (!data.suggestions || data.suggestions.length === 0) {
                    return;
                }

                data.suggestions.forEach(function (value) {

                    const item = document.createElement("div");

                    item.className = "suggestion-item";
                    item.textContent = value;

                    item.addEventListener("mousedown", function (event) {
                        event.preventDefault();

                        input.value = value;
                        suggestionsBox.innerHTML = "";

                        input.dispatchEvent(
                            new Event("change", {
                                bubbles: true
                            })
                        );
                    });

                    suggestionsBox.appendChild(item);
                });

            } catch (error) {

                console.error(
                    "Suggestion request failed:",
                    error
                );

            }
        }


        // ---------------------------------
        // TYPING
        // ---------------------------------

        input.addEventListener("input", function () {

            const query = this.value.trim();

            loadSuggestions(query);

        });


        // ---------------------------------
        // CLICK / FOCUS
        // Show available options even
        // when the field is empty
        // ---------------------------------

        input.addEventListener("focus", function () {

            loadSuggestions(this.value.trim());

        });


        // ---------------------------------
        // HIDE WHEN CLICKING OUTSIDE
        // ---------------------------------

        document.addEventListener("click", function (event) {

            if (
                event.target !== input &&
                !suggestionsBox.contains(event.target)
            ) {
                suggestionsBox.innerHTML = "";
            }

        });
    }


    // ---------------------------------
    // BRAND
    // ---------------------------------

    setupAutocomplete(
        "id_brand",
        "brand-suggestions",
        "brand"
    );


    // ---------------------------------
    // MODEL
    // Filter models using selected brand
    // ---------------------------------

    setupAutocomplete(
        "id_model",
        "model-suggestions",
        "model",
        function () {

            const brandInput =
                document.getElementById("id_brand");

            return {
                brand: brandInput
                    ? brandInput.value.trim()
                    : ""
            };
        }
    );


    // ---------------------------------
    // FUEL TYPE
    // ---------------------------------

    setupAutocomplete(
        "id_fuel_type",
        "fuel-suggestions",
        "fuel_type"
    );


    // ---------------------------------
    // TRANSMISSION
    // ---------------------------------

    setupAutocomplete(
        "id_transmission",
        "transmission-suggestions",
        "transmission"
    );


    // ---------------------------------
    // CONDITION
    // ---------------------------------

    setupAutocomplete(
        "id_condition",
        "condition-suggestions",
        "condition"
    );


    // ---------------------------------
    // LOCATION
    // ---------------------------------

    setupAutocomplete(
        "id_location",
        "location-suggestions",
        "location"
    );

});

    async function setupNumericRange(
        inputId,
        field,
        hintId
    ) {
        const input = document.getElementById(inputId);
        const hint = document.getElementById(hintId);

        if (!input || !hint) {
            console.log("Missing:", inputId, hintId);
            return;
        }

        try {
            const response = await fetch(
                `/api/vehicle-suggestions/?field=${field}`
            );

            const data = await response.json();

            console.log(field, data);

            if (data.min !== undefined && data.max !== undefined) {
                hint.textContent =
                    `Dataset range: ${data.min} - ${data.max}`;

                input.min = data.min;
                input.max = data.max;
            }

        } catch (error) {
            console.error(
                `Failed to load ${field} range:`,
                error
            );
        }
    }


    setupNumericRange(
        "id_year",
        "year",
        "year-hint"
    );

    setupNumericRange(
        "id_mileage",
        "mileage",
        "mileage-hint"
    );

    setupNumericRange(
        "id_engine_capacity",
        "engine_capacity",
        "engine-hint"
    );