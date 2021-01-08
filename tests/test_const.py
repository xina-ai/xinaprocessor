#region example 1
text_test_example_1 = "نص عربي english text"
example_1_remove_english_text = "نص عربي"
#endregion 

#region example 2
text_test_example_2 = "@نص_عربي #نص_عربي نص عربي"
example_2_remove_english_text = text_test_example_2
#endregion 

#region example 3
text_test_example_3 = "نص.عربي؟"
example_3_remove_english_text = text_test_example_3
#endregion 

#region example 4
text_test_example_4 = "نص عربي ملتصق بـ English Text"
example_4_remove_english_text = "نص عربي ملتصق بـ"
#endregion 
text_test_example_5 = "Only English Text"
text_test_example_6 = "123!"
text_test_example_7 = "نص عربيhttps://www.youtube.com/"
text_test_example_8 = "هذا نص عربي \t هذا نص عربي \t هل هذا نص عربي؟ \t this is english text \t ٥ \t 4 \t 4?! \t 漢"
text_test_example_9 = "漢 \n 漢 \n \n 漢 \n 65 \n \t \n ح"
text_test_example_10 = " نص عربي يحتوي \n أحد سطوره \n على A- \n أ \n ا \n آ \n ن"
text_test_example_11 = "گردد"
text_test_example_12 = "1) نص عربي. \n 2) نص عربي?! \n "
text_test_example_13 = "هذا النص عربي This is an English Text 123456789 !@#$%^&*)(_+ 漢字 ٤٥٦ https://www.youtube.com/"

list_test_example_1 = [text_test_example_1]
list_test_example_2 = ["نص عربي 1",
                        "نص عربي 2",
                        "english text",
                        "نص عربيــ and this english",
                        "漢",
                        "#$%^",
                        "#نص_عربي"]