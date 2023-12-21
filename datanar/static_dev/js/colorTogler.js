/*!
 * Color mode toggler for Bootstrap's docs (https://getbootstrap.com/)
 * Copyright 2011-2023 The Bootstrap Authors
 * Licensed under the Creative Commons Attribution 3.0 Unported License.
 */

(() => {
  "use strict";

  const getStoredTheme = () => localStorage.getItem("theme");
  const setStoredTheme = theme => localStorage.setItem("theme", theme);

  function setColors(mode) {
    let btnOutlineOriginal, btnOutlineNew, btnOriginal, btnNew, textOriginal, textNew;

    if (mode === "light") {
      btnOutlineOriginal = "btn-outline-light";
      btnOutlineNew = "btn-outline-dark";
      btnOriginal = "btn-light";
      btnNew = "btn-dark";
      textOriginal = "text-light";
      textNew = "text-dark";
    } else {
      btnOutlineOriginal = "btn-outline-dark";
      btnOutlineNew = "btn-outline-light";
      btnOriginal = "btn-dark";
      btnNew = "btn-light";
      textOriginal = "text-dark";
      textNew = "text-light";
    }

    document.querySelectorAll(`.${btnOutlineOriginal}`).forEach(element => {
      element.classList.remove(btnOutlineOriginal);
      element.classList.add(btnOutlineNew);
    });

    document.querySelectorAll(`.${btnOriginal}`).forEach(element => {
      element.classList.remove(btnOriginal);
      element.classList.add(btnNew);
    });

    document.querySelectorAll(`.${textOriginal}`).forEach(element => {
      element.classList.remove(textOriginal);
      element.classList.add(textNew);
    });
  }

  const getPreferredTheme = () => {
    const storedTheme = getStoredTheme();
    if (storedTheme) {
      return storedTheme;
    }

    return window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light";
  }

  const setTheme = theme => {
    if (theme === "auto" && window.matchMedia("(prefers-color-scheme: dark)").matches) {
      document.documentElement.setAttribute("data-bs-theme", "dark");
      setColors("dark");
    } else {
      document.documentElement.setAttribute("data-bs-theme", theme);
      setColors(theme);
    }
  }

  setTheme(getPreferredTheme());

  const showActiveTheme = (theme, focus = false) => {
    const themeSwitcher = document.querySelector("#bd-theme");

    if (!themeSwitcher) {
      return;
    }

    const themeSwitcherText = document.querySelector('#bd-theme-text');
    const activeThemeIcon = document.querySelector("#theme-icon-active");

    const btnToActive = document.querySelector(`[data-bs-theme-value="${theme}"]`);
    const svgOfActiveBtn = btnToActive.querySelector("i").getAttribute("class")

    document.querySelectorAll('[data-bs-theme-value]').forEach(element => {
      element.classList.remove("active")
      element.setAttribute("aria-pressed", "false")
    })

    btnToActive.classList.add("active");
    btnToActive.setAttribute("aria-pressed", "true");
    activeThemeIcon.setAttribute("class", svgOfActiveBtn);
    const themeSwitcherLabel = `${themeSwitcherText.textContent} (${btnToActive.dataset.bsThemeValue})`;
    themeSwitcher.setAttribute("aria-label", themeSwitcherLabel);

    if (focus) {
      themeSwitcher.focus();
    }
  }

  window.matchMedia("(prefers-color-scheme: dark)").addEventListener("change", () => {
    const storedTheme = getStoredTheme();
    if (storedTheme !== "light" && storedTheme !== "dark") {
      setTheme(getPreferredTheme());
    }
  });

  window.addEventListener("DOMContentLoaded", () => {
    const preferredTheme = getPreferredTheme();
    setTheme(preferredTheme);
    showActiveTheme(preferredTheme);

    document.querySelectorAll('[data-bs-theme-value]')
      .forEach(toggle => {
        toggle.addEventListener("click", () => {
          const theme = toggle.getAttribute("data-bs-theme-value");
          setStoredTheme(theme);
          setTheme(theme);
          showActiveTheme(theme, true);
        });
      });
  });
})()
