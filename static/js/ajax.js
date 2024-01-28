$(document).ready(function() {
    var generatedAssignment = false;
    var generatedEssay = false;
    var contentType = "";

    var isRecording = false; // Track recording state

$("#voiceInputBtn").click(function() {
    var recognition = new webkitSpeechRecognition();
    recognition.onresult = function(event) {
        var transcript = event.results[0][0].transcript;
        $("#topicInput").val(transcript);
    };

    var micSvg = $("#mic-svg"); // Get the SVG element

    if (!isRecording) {
        // Add the pulse animation class when recording starts
        micSvg.addClass("pulse-animation");
    }

    recognition.onstart = function() {
        isRecording = true;
    };

    recognition.onend = function() {
        isRecording = false;
        // Remove the pulse animation class when recording stops
        micSvg.removeClass("pulse-animation");
    };

    recognition.start();
});

    
        

    function showLoader() {
        const loader = document.getElementById("loader");
        if (loader) {
            loader.style.display = "block";
        }
    }

    function hideLoader() {
        const loader = document.getElementById("loader");
        if (loader) {
            loader.style.display = "none";
        }
    }

    function generateContent(url, title, target) {
        var topic = $("#topicInput").val();
        var wordCount = $("#wordCountInput").val();
        topic = encodeURIComponent(topic);
    
        // Check if the topic input is empty
        if (topic.trim() === "") {
            $("#empty").html("Please enter a topic before generating " + title.toLowerCase() + ".");
            // Hide the loader if it's displayed
            hideLoader();
            return; // Exit the function
        }

        // Remove the message
        $("#empty").html("");
        
        // Show the loader
        showLoader();
    
        $.ajax({
            url: url,
            data: { topic: topic, word_count: wordCount },
            dataType: "json",
            success: function(data) {
                var generatedText;
                if (contentType === "assignment") {
                    generatedText = data.assignment_text;
                    generatedAssignment = true; // Set to true upon successful generation
                    generatedEssay = false; // Reset the other flag
                } else if (contentType === "essay") {
                    generatedText = data.essay_text;
                    generatedAssignment = false; // Reset the other flag
                    generatedEssay = true; // Set to true upon successful generation
                }
    
                var sanitizedText = $("<div>").text(generatedText).html();
    
                // Process the content
                var sections = sanitizedText.split('\n'); // Split into sections
    
                var formattedText = "<h1 class='custom-h1'>" + title + "</h1>";
    
                // Process sections
                for (var i = 0; i < sections.length; i++) {
                    formattedText += "<p class='custom-p'>" + sections[i] + "</p>";
                }
    
                $(target).html(formattedText);
                hideLoader();
                removeRegenerateLoader();
            },
            error: function() {
                $(target).html("Error: Failed to generate the " + title.toLowerCase() + ". Please try again later.");
                hideLoader();
            }
        });
    }
    

    $("#assignmentBtn").click(function() {
        contentType = "assignment";
        generateContent("/generate-assignment/", "Assignment", "#textOutput");
    });

    $("#essayBtn").click(function() {
        contentType = "essay";
        generateContent("/generate-essay/", "Essay", "#textOutput");
    });


    
    function addRegenerateLoader() {
        var regenerateLoader = $("#regenerateloader");
        regenerateLoader.addClass("regenerate-loader");
    }
    

    // Function to remove the regenerate-loader class
    function removeRegenerateLoader() {
        var loader = $(".regenerate-loader");

        // Remove the loader from the DOM
        loader.remove();
    }

    $("#regenerateBtn").click(function() {
        if ((contentType === "assignment" && generatedAssignment) || (contentType === "essay" && generatedEssay)) {
            if (contentType === "assignment") {
                // Add the regenerate loader
                addRegenerateLoader();

                // Generate content asynchronously
                generateContent("/generate-assignment/", "Regenerated Assignment", "#textOutput", function() {
                    // Remove the regenerate loader when content regeneration is complete
                    removeRegenerateLoader();
                });
            } else if (contentType === "essay") {
                // Add the regenerate loader
                addRegenerateLoader();

                // Generate content asynchronously
                generateContent("/generate-essay/", "Regenerated Essay", "#textOutput", function() {
                    // Remove the regenerate loader when content regeneration is complete
                    removeRegenerateLoader();
                });
            }
        } else {
            $("#textOutput").html("Please generate content first before clicking the 'Regenerate' button.");
        }
    });

    $("#downloadPdfBtn").click(function() {
        window.location.href = "/download-pdf/";
        setTimeout(function() {
            location.reload();
        }, 1000);
    });
});
