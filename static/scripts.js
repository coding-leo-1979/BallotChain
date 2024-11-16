/* Javascript 파일 */
document.addEventListener("DOMContentLoaded", () => {
    // 회원가입 요청
    const registerForm = document.getElementById("registerForm");
    if (registerForm) {
        registerForm.addEventListener("submit", async (e) => {
            e.preventDefault();
            const username = document.getElementById("username").value;
            const password = document.getElementById("password").value;
            const birthday = document.getElementById("birthday").value;

            try {
                const response = await fetch("/api/auth/register", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ username, password, birthday }),
                });
                const result = await response.json();
                document.getElementById("responseMessage").innerText = result.message || result.error;
            } catch (error) {
                console.error("Error:", error);
                document.getElementById("responseMessage").innerText = "서버 오류가 발생했습니다.";
            }
        });
    }

    // 이메일 인증 요청
    const emailForm = document.getElementById("emailForm");
    if (emailForm) {
        emailForm.addEventListener("submit", async (e) => {
            e.preventDefault();
            const email = document.getElementById("email").value;

            try {
                const response = await fetch("/api/auth/verify-email", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ email }),
                });
                const result = await response.json();
                document.getElementById("responseMessage").innerText = result.success
                    ? "인증 이메일이 발송되었습니다."
                    : result.error;
            } catch (error) {
                console.error("Error:", error);
                document.getElementById("responseMessage").innerText = "서버 오류가 발생했습니다.";
            }
        });
    }

    // 이메일 확인 요청
    const confirmEmailForm = document.getElementById("confirmEmailForm");
    if (confirmEmailForm) {
        confirmEmailForm.addEventListener("submit", async (e) => {
            e.preventDefault();
            const email = document.getElementById("email").value;
            const token = document.getElementById("token").value;

            try {
                const response = await fetch("/api/auth/confirm-email", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ email, token }),
                });
                const result = await response.json();
                document.getElementById("responseMessage").innerText = result.success
                    ? "이메일 인증이 완료되었습니다."
                    : result.error;
            } catch (error) {
                console.error("Error:", error);
                document.getElementById("responseMessage").innerText = "서버 오류가 발생했습니다.";
            }
        });
    }
});




