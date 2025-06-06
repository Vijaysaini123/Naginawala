<?php
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    // Sanitize and validate inputs
    $name = htmlspecialchars(trim($_POST["name"]));
    $email = filter_var(trim($_POST["email"]), FILTER_SANITIZE_EMAIL);
    $subject = htmlspecialchars(trim($_POST["subject"]));
    $message = htmlspecialchars(trim($_POST["message"]));

    // Validate required fields and email format
    if ($name && $email && $subject && $message && filter_var($email, FILTER_VALIDATE_EMAIL)) {
        $to = "engineer.vijaysaini@gmail.com";  // Your email address
        $email_subject = "Contact Form Submission: $subject";
        $email_body = "You have received a new message from your website contact form.\n\n".
                      "Here are the details:\n".
                      "Name: $name\n".
                      "Email: $email\n".
                      "Subject: $subject\n".
                      "Message:\n$message\n";

        $headers = "From: $email\r\n";
        $headers .= "Reply-To: $email\r\n";

        // Send email
        if (mail($to, $email_subject, $email_body, $headers)) {
            // Redirect to thank you page or display success message
            echo "<script>alert('Thank you for contacting us. We will get back to you soon.'); window.location.href='contact.html';</script>";
        } else {
            echo "<script>alert('Sorry, there was an error sending your message. Please try again later.'); window.location.href='contact.html';</script>";
        }
    } else {
        echo "<script>alert('Please fill in all fields correctly.'); window.location.href='contact.html';</script>";
    }
} else {
    // If accessed directly without POST, redirect back to contact form
    header("Location: contact.html");
    exit();
}
?>
