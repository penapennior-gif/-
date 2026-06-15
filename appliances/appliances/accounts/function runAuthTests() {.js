function runAuthTests() {
  console.log('🧪 Запуск тестов системы регистрации...\n');
  let passed = 0;
  let failed = 0;

  // Вспомогательная функция для красивого вывода
  function assert(description, condition) {
    if (condition) {
      console.log(`✅ [PASS] ${description}`);
      passed++;
    } else {
      console.error(`❌ [FAIL] ${description}`);
      failed++;
    }
  }

  // --- ТЕСТ 1: Регистрация со специальным кодом ---
  const userWithCode = { username: 'Ivan', promoCode: 'VIP2024' };
  assert(
    'Пользователь с кодом должен иметь доступ к заявкам',
    canAccessApplications(userWithCode) === true
  );

  // --- ТЕСТ 2: Регистрация без кода ---
  const userWithoutCode = { username: 'Oleg', promoCode: undefined };
  assert(
    'Пользователь без кода НЕ должен иметь доступ к заявкам',
    canAccessApplications(userWithoutCode) === false
  );

  // --- ТЕСТ 3: Регистрация с пустым кодом (строка с пробелом) ---
  const userWithEmptyCode = { username: 'Anna', promoCode: '   ' };
  assert(
    'Пользователь с пустым кодом (пробелы) НЕ должен иметь доступ',
    canAccessApplications(userWithEmptyCode) === false
  );

  // --- ТЕСТ 4: Регистрация с пустой строкой ---
  const userWithEmptyString = { username: 'Dmitry', promoCode: '' };
  assert(
    'Пользователь с пустой строкой НЕ должен иметь доступ',
    canAccessApplications(userWithEmptyString) === false
  );

  // Итоговая статистика
  console.log('\n------------------------------');
  console.log(`📊 Итог: Пройдено: ${passed}, Про�
JavaScript

�алено: ${failed}`);
  console.log('------------------------------');
}

// Запуск
runAuthTests();